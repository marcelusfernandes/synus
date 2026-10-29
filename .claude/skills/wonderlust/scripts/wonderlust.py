#!/usr/bin/env python3
"""wonderlust: cria, monta e valida bibliotecas de referência de produto no formato vicaura/wonderful.

Uso:
  wonderlust.py init <url|documento> --product NOME [--slug S] [--root DIR] [--feature NOME ...]
                [--skip CATEGORIA ...] [--generator G] [--date AAAA-MM-DD] [--lede TEXTO] [--own-product]
  wonderlust.py build <pasta-da-biblioteca>
  wonderlust.py check <pasta-da-biblioteca> [--strict]

O agente escreve só o frontmatter e o corpo (entre os marcadores) de cada documento.
Tudo o mais (cabeçalho, alertas de ressalva, READMEs, manifest.json) é gerado por `build`.
"""
import argparse
import datetime
import json
import os
import posixpath
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
TAXONOMY = json.loads((HERE.parent / "assets" / "taxonomy.json").read_text(encoding="utf-8"))
ARCH = TAXONOMY["archetypes"]
TAX_CATS = {c["id"]: c for c in TAXONOMY["categories"]}
KINDS = TAXONOMY["caveat_kinds"]
STATUSES = ("sufficient", "limited")
LANG_LABEL = {"en": "inglês", "pt": "português", "es": "espanhol"}

START_RE = re.compile(r"^<!-- início do conteúdo original.*-->[ \t]*$", re.M)
END_MARK = "<!-- fim do conteúdo original -->"
FM_ORDER = ["id", "title", "category", "status", "confidence", "generated", "source",
            "generator", "language", "sources", "caveats"]
REQUIRED_FM = ["id", "title", "category", "status", "confidence", "generated", "source",
               "generator", "language", "caveats"]
SUMMARY_LEN = 237  # reproduz os resumos da Vicaura (corte na última palavra inteira)


class DocError(Exception):
    pass


# ---------------------------------------------------------------- utilities

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", " ", s.lower()).replace("_", " ")
    return re.sub(r"[\s-]+", "-", s).strip("-")


def q(s):
    return json.dumps(s, ensure_ascii=False)


def bare_or_quoted(v):
    if isinstance(v, bool) or v is None:
        return q(v)
    if isinstance(v, (int, float)):
        return repr(v)
    v = str(v)
    if re.fullmatch(r"[A-Za-z0-9][\w./:#?=&%~+@-]*", v) and ": " not in v and " #" not in v \
            and v.lower() not in ("true", "false", "null", "yes", "no", "on", "off"):
        return v
    return q(v)


def domain_of(url):
    host = urlparse(url).netloc or url
    return host[4:] if host.startswith("www.") else host


def is_url(s):
    return str(s).startswith(("http://", "https://"))


def valid_source(root, s):
    """URL http(s) ou caminho relativo a um documento-fonte guardado na biblioteca (modo documento interno)."""
    if is_url(s):
        return True
    s = str(s)
    return bool(s) and not s.startswith("/") and ".." not in s.split("/") and (Path(root) / s).is_file()


def rel_link(from_path, to_path):
    return posixpath.relpath(to_path, posixpath.dirname(from_path) or ".")


# ---------------------------------------------------------------- frontmatter

def _scalar(v):
    v = v.strip()
    if v == "[]":
        return []
    if v.startswith('"'):
        return json.loads(v)
    if v.startswith("'") and v.endswith("'") and len(v) >= 2:
        return v[1:-1].replace("''", "'")
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    if v in ("true", "false"):
        return v == "true"
    if v in ("null", "~"):
        return None
    return v


def _mini_yaml(s):
    """Parser estrito para o subconjunto de YAML que o build escreve."""
    data, lines, i = {}, s.split("\n"), 0
    key_re = r"([A-Za-z_][\w-]*)"
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.fullmatch(key_re + r":(?:[ \t]+(.*))?", line)
        if not m:
            raise ValueError(f"linha não suportada: {line!r}")
        key, val = m.group(1), m.group(2)
        i += 1
        if val is not None and val.strip():
            data[key] = _scalar(val)
            continue
        items = []
        while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            m2 = re.fullmatch(r"  - (.*)", line)
            if not m2:
                raise ValueError(f"item de lista não suportado: {line!r}")
            m3 = re.fullmatch(key_re + r":[ \t]+(.*)", m2.group(1))
            i += 1
            if not m3:
                items.append(_scalar(m2.group(1)))
                continue
            item = {m3.group(1): _scalar(m3.group(2))}
            while i < len(lines) and lines[i].startswith("    "):
                m4 = re.fullmatch(r"    " + key_re + r":[ \t]+(.*)", lines[i])
                if not m4:
                    raise ValueError(f"campo não suportado: {lines[i]!r}")
                item[m4.group(1)] = _scalar(m4.group(2))
                i += 1
            items.append(item)
        data[key] = items
    return data


def load_frontmatter(s):
    try:
        return _mini_yaml(s)
    except (ValueError, json.JSONDecodeError) as e:
        try:
            import yaml  # fallback para YAML válido fora do subconjunto
        except ImportError:
            raise DocError(f"frontmatter fora do formato suportado ({e})")
        try:
            data = yaml.safe_load(s) or {}
        except yaml.YAMLError as ye:
            raise DocError(f"frontmatter inválido: {ye}")

        def norm(x):
            if isinstance(x, (datetime.date, datetime.datetime)):
                return x.isoformat()[:10]
            if isinstance(x, list):
                return [norm(y) for y in x]
            if isinstance(x, dict):
                return {k: norm(v) for k, v in x.items()}
            return x
        return norm(data)


def dump_frontmatter(fm):
    out = ["---"]
    keys = [k for k in FM_ORDER if k in fm] + [k for k in fm if k not in FM_ORDER]
    for k in keys:
        v = fm[k]
        if k == "title":
            out.append(f"title: {q(str(v))}")
        elif k == "caveats":
            if not v:
                out.append("caveats: []")
                continue
            out.append("caveats:")
            for c in v:
                out.append(f"  - kind: {c.get('kind', '')}")
                out.append(f"    title: {q(str(c.get('title', '')))}")
                out.append(f"    text: {q(str(c.get('text', '')))}")
                if c.get("link"):
                    out.append(f"    link: {c['link']}")
                for ek, ev in c.items():
                    if ek not in ("kind", "title", "text", "link"):
                        out.append(f"    {ek}: {bare_or_quoted(ev)}")
        elif isinstance(v, list):
            if not v:
                out.append(f"{k}: []")
            else:
                out.append(f"{k}:")
                out += [f"  - {bare_or_quoted(x)}" for x in v]
        else:
            out.append(f"{k}: {bare_or_quoted(v)}")
    out.append("---")
    return "\n".join(out)


# ---------------------------------------------------------------- documents

def parse_doc(text):
    if not text.startswith("---\n"):
        raise DocError("o arquivo não começa com frontmatter (---)")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise DocError("frontmatter sem o --- de fechamento")
    fm = load_frontmatter(text[4:end])
    rest = text[end + 5:]
    m = START_RE.search(rest)
    if not m:
        raise DocError("marcador '<!-- início do conteúdo original ... -->' ausente")
    after = rest[m.end():]
    e = after.find(END_MARK)
    if e < 0:
        raise DocError(f"marcador '{END_MARK}' ausente")
    return {"fm": fm, "start": m.group(0).rstrip(), "body": after[:e].strip("\n")}


def first_paragraph(body):
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    for block in re.split(r"\n\s*\n", body):
        lines = [l.strip() for l in block.split("\n") if l.strip() and not l.lstrip().startswith("#")]
        if lines:
            return " ".join(lines)
    return ""


def summary_of(body):
    s = first_paragraph(body)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "").replace("__", "").replace("`", "")
    s = re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= SUMMARY_LEN:
        return s
    return s[:SUMMARY_LEN].rsplit(" ", 1)[0] + "…"


def flags(fm):
    return [c for c in fm.get("caveats") or [] if c.get("kind") != "evidence"]


def n_ressalvas(n):
    return f"{n} {'ressalva' if n == 1 else 'ressalvas'}"


class Library:
    def __init__(self, root):
        self.root = Path(root).resolve()
        mpath = self.root / "manifest.json"
        if not mpath.exists():
            raise SystemExit(f"manifest.json não encontrado em {self.root} (rode `init` primeiro)")
        self.manifest = json.loads(mpath.read_text(encoding="utf-8"))
        self.errors, self.warnings = [], []
        self.docs = []  # dicts: id, cat, path, fm, start, body
        self.cats = self.manifest.get("categories", [])
        self.pending = self.manifest.get("pending", [])
        self.cat_by_id = {c["id"]: c for c in self.cats}
        self._load_docs()

    def err(self, where, msg):
        self.errors.append((where, msg))

    def warn(self, where, msg):
        self.warnings.append((where, msg))

    def _load_docs(self):
        for c in self.cats:
            d = self.root / c["id"]
            if not d.is_dir():
                self.err(f"{c['id']}/", "pasta da categoria não existe")
                continue
            for p in sorted(d.glob("*.md")):
                if p.name == "README.md":
                    continue
                rel = f"{c['id']}/{p.name}"
                try:
                    doc = parse_doc(p.read_text(encoding="utf-8"))
                except DocError as e:
                    self.err(rel, str(e))
                    continue
                doc.update(id=p.stem, cat=c["id"], path=rel)
                self.docs.append(doc)
        self._sort_docs()
        self.doc_by_id = {}
        for d in self.docs:
            if d["id"] in self.doc_by_id:
                self.err(d["path"], f"id duplicado: '{d['id']}' também existe em {self.doc_by_id[d['id']]['path']}")
            self.doc_by_id.setdefault(d["id"], d)

    def _sort_docs(self):
        cat_order = {c["id"]: i for i, c in enumerate(self.cats)}

        def key(d):
            tax = TAX_CATS.get(d["cat"])
            fixed = [x["id"] for x in tax["docs"]] if tax else []
            if tax and tax.get("dynamic"):
                conf = d["fm"].get("confidence")
                conf = conf if isinstance(conf, (int, float)) else 0
                within = (0, -conf, str(d["fm"].get("title", d["id"])).lower())
            elif d["id"] in fixed:
                within = (0, fixed.index(d["id"]), "")
            else:
                within = (1, 0, d["id"])
            return (cat_order.get(d["cat"], 99), within)
        self.docs.sort(key=key)

    def docs_in(self, cat_id):
        return [d for d in self.docs if d["cat"] == cat_id]

    # ------------------------------------------------------------ rendering

    def doc_link(self, from_path, doc_id):
        d = self.doc_by_id[doc_id]
        return f"[{d['fm'].get('title', doc_id)}]({rel_link(from_path, d['path'])})"

    def caveat_line(self, c, from_path, where=None):
        kind = c.get("kind", "")
        head = f"**{KINDS.get(kind, {}).get('tag', kind)} · {c.get('title', '')}.**"
        loc = f" ({self.doc_link(from_path, where)})" if where else ""
        see = f" Ver também: {self.doc_link(from_path, c['link'])}." if c.get("link") in self.doc_by_id else ""
        return f"{head}{loc} {c.get('text', '')}{see}"

    def render_doc(self, d):
        fm, cat = d["fm"], self.cat_by_id[d["cat"]]
        conf = fm.get("confidence")
        conf_txt = f"{conf:.2f}" if isinstance(conf, (int, float)) else str(conf)
        n = len(flags(fm))
        meta = (f"[{self.manifest['product']}](../README.md) / [{cat['label']}](README.md) · "
                f"`{fm.get('status')}` · confiança {conf_txt} · gerado {fm.get('generated')}"
                + (f" · {n_ressalvas(n)}" if n else ""))
        parts = [dump_frontmatter(fm), f"# {fm.get('title', d['id'])}", meta]
        for c in fm.get("caveats") or []:
            alert = KINDS.get(c.get("kind"), {}).get("alert", "NOTE")
            parts.append(f"> [!{alert}]\n> {self.caveat_line(c, d['path'])}")
        parts += [d["start"], d["body"], END_MARK]
        if any(c.get("kind") == "truncated" for c in fm.get("caveats") or []):
            parts.append("> [!CAUTION]\n> O arquivo original termina aqui, no meio da frase.")
        return "\n\n".join(parts) + "\n"

    def render_category(self, c):
        ds = self.docs_in(c["id"])
        lines = [f"# {c['label']}", "", f"[{self.manifest['product']}](../README.md) / {c['name']}", "",
                 c["blurb"], ""]
        if c.get("note"):
            lines += ["> [!WARNING]", f"> **Atenção.** {c['note']}", ""]
        lines += [f"## Documentos ({len(ds)})", ""]
        for d in ds:
            fm = d["fm"]
            n = len(flags(fm))
            conf = fm.get("confidence")
            conf_txt = f"{conf:.2f}" if isinstance(conf, (int, float)) else str(conf)
            extra = f" · {n_ressalvas(n)}" if n else ""
            lines.append(f"- **[{fm.get('title', d['id'])}]({posixpath.basename(d['path'])})** — "
                         f"`{fm.get('status')}` · confiança {conf_txt}{extra}  ")
            lines.append(f"  {summary_of(d['body'])}")
        return "\n".join(lines) + "\n"

    def render_pending(self, p):
        return "\n".join([
            f"# {p['label']}", "", f"[{self.manifest['product']}](../README.md) / {p['name']}", "",
            "> [!NOTE]",
            "> **Ainda não gerado.** Os arquivos desta categoria ainda não foram produzidos.", "",
            "## Documentos esperados", "",
            *[f"- {x['title']} → `{posixpath.basename(x['path'])}`" for x in p.get("docs", [])],
        ]) + "\n"

    def render_readme(self):
        m = self.manifest
        product, source = m["product"], m["source"]
        domain = domain_of(source) if is_url(source) else posixpath.basename(source)
        total = len(self.docs)
        limited = sum(d["fm"].get("status") == "limited" for d in self.docs)
        rows = []
        for c in self.cats:
            ds = self.docs_in(c["id"])
            suff = sum(d["fm"].get("status") == "sufficient" for d in ds)
            rows.append(f"| [{c['label']}]({c['id']}/README.md) | {c['blurb']} | {len(ds)} | {suff} | {len(ds) - suff} |")
        for p in self.pending:
            names = ", ".join(x["title"] for x in p.get("docs", []))
            rows.append(f"| [{p['label']}]({p['id']}/README.md) | Ainda não gerado ({names}). | 0 | — | — |")

        cav = ["- " + self.caveat_line(c, "README.md") for c in m.get("caveats", [])]
        seen, pairs = set(), set()
        for d in self.docs:
            for c in flags(d["fm"]):
                pair = frozenset((d["id"], c["link"])) if c.get("kind") == "conflict" and c.get("link") else None
                if c.get("text") in seen or (pair and pair in pairs):
                    continue  # mesmo texto, ou o lado recíproco de um conflito já listado
                seen.add(c.get("text"))
                if pair:
                    pairs.add(pair)
                cav.append("- " + self.caveat_line(c, "README.md", where=d["id"]))
        if not cav:
            cav = ["Nenhuma ressalva registrada."]

        dirs = [(c["id"], len(self.docs_in(c["id"]))) for c in self.cats] + [(p["id"], 0) for p in self.pending]
        tree = [f"{self.root.name}/",
                "├── README.md              # esta visão geral",
                "├── manifest.json          # metadados de categorias, documentos e ressalvas"]
        if (self.root / "fontes").is_dir():
            tree.append("├── fontes/                # documentos-fonte internos (modo documento interno)")
        if m.get("own_product"):
            notice = (f"> **Produto próprio.** Estes arquivos descrevem {product} a partir de documentos internos. "
                      "O que é proposta ou rascunho está marcado como tal: não trate como fato de mercado.")
        else:
            notice = (f"> **Produto de referência.** Estes arquivos descrevem {product}, não o nosso produto. "
                      "Use como exemplo, benchmark ou evidência de mercado.")
        for i, (cid, n) in enumerate(dirs):
            branch = "└──" if i == len(dirs) - 1 else "├──"
            tree.append(f"{branch} {cid}/".ljust(42) + (f"# {n} docs + README.md" if n else "# placeholder"))

        pending_note = ""
        if self.pending:
            items = "; ".join(f"{p['name']} ({', '.join(x['title'] for x in p.get('docs', []))})" for p in self.pending)
            pending_note = f"\n> [!NOTE]\n> **Ainda não gerado:** {items}.\n"

        lede = m.get("lede", "").strip()
        origin = m.get("origin_artifact")
        lang = LANG_LABEL.get(m.get("language", "en"), m.get("language", "en"))
        footer = (f"Arquivos gerados por {m['generator']} em {m['generated']} (UTC). Conteúdo dos documentos em {lang}."
                  + (f" Migrado do artifact [{product} Reference]({origin})." if origin else ""))

        return f"""# {product}

> Arquivos de referência sobre {product} ([{domain}]({source})), gerados por {m['generator']} e organizados por categoria.
{chr(10) + lede + chr(10) if lede else ""}
| Fonte | Gerado | Documentos | Limited |
|---|---|---|---|
| [{domain}]({source}) | {m['generated']} UTC | {total} | {limited} |

> [!IMPORTANT]
{notice}

## Categorias

| Categoria | Descrição | Docs | Sufficient | Limited |
|---|---|---|---|---|
{chr(10).join(rows)}

## Como ler a confiabilidade

- **`sufficient`**: há evidência suficiente para sustentar o arquivo.
- **`limited`**: menos evidência. Afirmações marcadas com *(Extrapolated)* são inferidas, não observadas.
- **Marcações**: em bibliotecas geradas pela skill wonderlust, toda afirmação inferida leva *(Extrapolated)*. Em arquivos legados (Vicaura) a marcação é inconsistente: um ponto sem marca não está necessariamente verificado.

Cada documento traz `status` e `confidence` (0 a 1) no frontmatter.

## Ressalvas conhecidas

Cada uma também aparece no topo do documento correspondente.

{chr(10).join(cav)}
{pending_note}
## Estrutura

```text
{chr(10).join(tree)}
```

Cada documento segue o mesmo formato:

1. **Frontmatter YAML**: `id`, `title`, `category`, `status`, `confidence`, `generated`, `source`, `generator`, `language`, `sources` (opcional) e `caveats` (lista de `kind`, `title`, `text` e, quando houver, `link` para o `id` de outro documento).
2. **Cabeçalho**: título, navegação e as ressalvas como alertas (`CAUTION` para conflito/truncado, `WARNING` para evidência fraca, `NOTE` para inferência/estranheza). Gerado pelo `build`.
3. **Conteúdo** entre os comentários `<!-- início do conteúdo original ... -->` e `<!-- fim do conteúdo original -->`.

Tipos de ressalva (`kind`): `evidence` (evidência fraca), `inferred` (inferido), `oddity` (estranheza), `conflict` (conflito entre arquivos), `truncated` (arquivo truncado).

---

{footer}
"""

    def render_manifest(self):
        m = dict(self.manifest)
        cats = []
        for c in self.cats:
            c2 = {k: v for k, v in c.items() if k not in ("path", "docs")}
            c2["path"] = f"{c['id']}/"
            c2["docs"] = [d["id"] for d in self.docs_in(c["id"])]
            cats.append(c2)
        m["categories"] = cats
        docs = []
        for d in self.docs:
            fm = d["fm"]
            entry = {"id": d["id"], "cat": d["cat"], "title": fm.get("title"), "status": fm.get("status"),
                     "confidence": fm.get("confidence"), "generated": fm.get("generated"),
                     "source": fm.get("source"), "path": d["path"], "summary": summary_of(d["body"])}
            if fm.get("sources"):
                entry["sources"] = fm["sources"]
            entry["caveats"] = fm.get("caveats") or []
            docs.append(entry)
        m["docs"] = docs
        order = ["product", "source", "generator", "generated", "language", "own_product", "lede", "origin_artifact",
                 "caveats", "categories", "pending", "docs"]
        out = {k: m[k] for k in order if k in m}
        out.update({k: v for k, v in m.items() if k not in out})
        return json.dumps(out, ensure_ascii=False, indent=2) + "\n"

    def plan(self):
        files = {}
        for d in self.docs:
            files[d["path"]] = self.render_doc(d)
        for c in self.cats:
            files[f"{c['id']}/README.md"] = self.render_category(c)
        for p in self.pending:
            files[f"{p['id']}/README.md"] = self.render_pending(p)
        files["README.md"] = self.render_readme()
        files["manifest.json"] = self.render_manifest()
        return files


# ---------------------------------------------------------------- init

def stub_body(title, focus, archetype, extra_subsections=None):
    a = ARCH[archetype]
    subs = dict(a.get("subsections", {}))
    subs.update(extra_subsections or {})
    out = [f"<!-- TODO foco: {focus} -->"]
    for s in a["sections"]:
        out += ["", f"## {s['title']}", "", f"<!-- TODO: {s['guide']} -->"]
        for sub in subs.get(s["title"], []):
            out += ["", f"### {sub}", "", "<!-- TODO -->"]
    return "\n".join(out)


def cmd_init(a):
    local_doc = Path(a.url) if Path(a.url).is_file() else None
    if local_doc:
        if not a.product:
            raise SystemExit("com documento interno como fonte, informe --product")
        source = f"fontes/{local_doc.name}"
        slug = a.slug or slugify(a.product)
    else:
        source = a.url if re.match(r"https?://", a.url) else "https://" + a.url
        if not urlparse(source).path:
            source += "/"
        slug = a.slug or slugify(domain_of(source).split(".")[0])
    lib = Path(a.root) / slug
    if local_doc:
        dest = lib / source
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            dest.write_bytes(local_doc.read_bytes())
            print(f"Documento-fonte copiado para {dest}")
    date = a.date or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    mpath = lib / "manifest.json"
    if mpath.exists():
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
        print(f"Biblioteca existente: {lib} (só stubs faltantes serão criados)")
    else:
        skip = set(a.skip or [])
        unknown = skip - set(TAX_CATS)
        if unknown:
            raise SystemExit(f"categoria(s) desconhecida(s) em --skip: {', '.join(sorted(unknown))}")
        cats, pending = [], []
        for c in TAXONOMY["categories"]:
            base = {"id": c["id"], "name": c["name"], "label": c["label"], "blurb": c["blurb"]}
            if c["id"] in skip:
                pending.append({**base, "path": f"{c['id']}/",
                                "docs": [{"id": x["id"], "title": x["title"], "path": f"{c['id']}/{x['id']}.md"}
                                         for x in c["docs"]]})
            else:
                cats.append({**base, "path": f"{c['id']}/", "docs": []})
        manifest = {"product": a.product or domain_of(source).split(".")[0].capitalize(), "source": source,
                    "generator": a.generator, "generated": date, "language": "en"}
        if a.own_product:
            manifest["own_product"] = True
        manifest.update({"lede": a.lede or "", "caveats": [], "categories": cats, "pending": pending, "docs": []})
        lib.mkdir(parents=True, exist_ok=True)
        mpath.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Biblioteca criada: {lib}")

    gen, lang = manifest["generator"], manifest.get("language", "en")
    start = f"<!-- início do conteúdo original gerado por {gen} ({LANG_LABEL.get(lang, lang)}) -->"
    created = []

    def make(cat_id, doc_id, title, focus, archetype, subs=None):
        p = lib / cat_id / f"{doc_id}.md"
        if p.exists():
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        fm = {"id": doc_id, "title": title, "category": cat_id, "status": "limited", "confidence": 0.0,
              "generated": manifest["generated"], "source": manifest["source"], "generator": gen,
              "language": lang, "sources": [], "caveats": []}
        text = "\n\n".join([dump_frontmatter(fm), f"# {title}", start,
                            stub_body(title, focus, archetype, subs), END_MARK]) + "\n"
        p.write_text(text, encoding="utf-8")
        created.append(f"{cat_id}/{doc_id}.md")

    active = {c["id"] for c in manifest["categories"]}
    for c in TAXONOMY["categories"]:
        if c["id"] not in active:
            continue
        (lib / c["id"]).mkdir(parents=True, exist_ok=True)
        for x in c["docs"]:
            make(c["id"], x["id"], x["title"], x["focus"], c["archetype"], x.get("subsections"))
    if a.feature:
        if "features" not in active:
            raise SystemExit("a categoria 'features' foi pulada; não dá para criar funcionalidades")
        for name in a.feature:
            make("features", slugify(name), name,
                 f"Feature spec for {name} as the source documents it; mark anything not documented as (Extrapolated).",
                 "feature")

    files = Library(lib).plan()
    for rel, content in files.items():
        if rel.endswith(".md") and rel.count("/") == 1 and not rel.endswith("README.md") and rel not in created:
            continue  # nunca reescreve documentos já existentes no init
        (lib / rel).parent.mkdir(parents=True, exist_ok=True)
        (lib / rel).write_text(content, encoding="utf-8")
    print(f"{len(created)} stub(s) criado(s).")
    for c in created:
        print("  +", c)
    print("Próximo passo: preencher frontmatter e corpo de cada stub, depois `build` e `check`.")


# ---------------------------------------------------------------- build / check

def cmd_build(a):
    lib = Library(a.library)
    if lib.errors:
        report(lib)
        raise SystemExit("build abortado: corrija os erros de leitura acima")
    changed = 0
    for rel, content in lib.plan().items():
        p = lib.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_text(encoding="utf-8") != content:
            p.write_text(content, encoding="utf-8")
            changed += 1
            print("  ~", rel)
    print(f"build ok: {len(lib.docs)} documentos, {changed} arquivo(s) atualizado(s).")


TERMINAL = tuple('.!?)"”’`*]')


def check_doc(lib, d):
    fm, where = d["fm"], d["path"]
    for k in REQUIRED_FM:
        if k not in fm:
            lib.err(where, f"frontmatter sem o campo '{k}'")
    if fm.get("id") not in (None, d["id"]):
        lib.err(where, f"id '{fm.get('id')}' diferente do nome do arquivo '{d['id']}'")
    if fm.get("category") not in (None, d["cat"]):
        lib.err(where, f"category '{fm.get('category')}' diferente da pasta '{d['cat']}'")
    status, conf = fm.get("status"), fm.get("confidence")
    if status not in STATUSES:
        lib.err(where, f"status inválido: {status!r} (use sufficient ou limited)")
    if not isinstance(conf, (int, float)) or isinstance(conf, bool) or not 0 < conf <= 1:
        lib.err(where, f"confidence não definido ou fora de (0, 1]: {conf!r}")
    else:
        if conf > 0.95:
            lib.warn(where, f"confidence {conf} acima do teto 0.95")
        if status == "sufficient" and conf < 0.86:
            lib.warn(where, f"status sufficient com confidence {conf} (< 0.86): considere limited")
        if status == "limited" and conf > 0.85:
            lib.warn(where, f"status limited com confidence {conf} (> 0.85): revise")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fm.get("generated", ""))):
        lib.err(where, f"generated deve ser AAAA-MM-DD: {fm.get('generated')!r}")
    if not valid_source(lib.root, fm.get("source", "")):
        lib.err(where, "source deve ser uma URL http(s) ou um arquivo existente em fontes/")
    if "sources" in fm:
        srcs = fm["sources"]
        if not isinstance(srcs, list) or not srcs:
            lib.warn(where, "sources vazio: liste as URLs (ou arquivos de fontes/) que sustentam o documento")
        elif any(not valid_source(lib.root, s) for s in srcs):
            lib.err(where, "sources deve conter URLs http(s) ou arquivos existentes em fontes/")
    cav = fm.get("caveats")
    if not isinstance(cav, list):
        lib.err(where, "caveats deve ser uma lista (use [] quando não houver)")
        cav = []
    for c in cav:
        if not isinstance(c, dict):
            lib.err(where, f"ressalva inválida: {c!r}")
            continue
        if c.get("kind") not in KINDS:
            lib.err(where, f"kind de ressalva inválido: {c.get('kind')!r} (use {', '.join(KINDS)})")
        if not c.get("title") or not c.get("text"):
            lib.err(where, "ressalva sem title ou text")
        link = c.get("link")
        if link and link not in lib.doc_by_id:
            lib.err(where, f"ressalva aponta para id inexistente: '{link}'")
        if c.get("kind") == "conflict" and link in lib.doc_by_id:
            back = lib.doc_by_id[link]["fm"].get("caveats") or []
            if not any(b.get("kind") == "conflict" for b in back):
                lib.warn(where, f"conflito com '{link}' sem ressalva conflict no outro documento")

    body = d["body"]
    if re.search(r"<!--\s*TODO", body) or re.search(r"\bTODO\b", body):
        lib.err(where, "ainda há TODO no corpo (stub não preenchido)")
    if re.search(r"^# ", body, re.M):
        lib.err(where, "o corpo não deve ter H1 (o título vem do frontmatter)")

    tax = TAX_CATS.get(d["cat"])
    if not tax:
        return
    arch = ARCH[tax["archetype"]]
    expected = [s["title"] for s in arch["sections"]]
    found = re.findall(r"^## (.+?)\s*$", body, re.M)
    low = [f.lower() for f in found]
    missing = [e for e in expected if e.lower() not in low]
    if missing:
        hint = ""
        h3 = [h.lower() for h in re.findall(r"^### (.+?)\s*$", body, re.M)]
        if any(m.lower() in h3 for m in missing):
            hint = " (estão como ###: promova para ##)"
        lib.err(where, f"seções ausentes: {', '.join(missing)}{hint}")
    else:
        order = [low.index(e.lower()) for e in expected]
        if order != sorted(order):
            lib.err(where, f"seções fora de ordem; esperado: {' / '.join(expected)}")
        for e in expected:
            f = found[low.index(e.lower())]
            if f != e:
                lib.warn(where, f"título de seção '{f}' deveria ser '{e}'")
    extra = [f for f in found if f.lower() not in [e.lower() for e in expected]]
    if extra:
        lib.warn(where, f"seções ## extras: {', '.join(extra)}")

    subs = dict(arch.get("subsections", {}))
    for x in tax["docs"]:
        if x["id"] == d["id"]:
            subs.update(x.get("subsections", {}))
    for sec, wanted in subs.items():
        m = re.search(rf"^## {re.escape(sec)}\s*$(.*?)(?=^## |\Z)", body, re.M | re.S | re.I)
        if not m:
            continue
        h3 = [h.lower() for h in re.findall(r"^#{3,4} (.+?)\s*$", m.group(1), re.M)]
        miss = [w for w in wanted if not any(h.startswith(w.lower()) for h in h3)]
        if miss:
            lib.warn(where, f"subseções ausentes em '{sec}': {', '.join(miss)}")

    text = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    words = len(re.findall(r"[A-Za-zÀ-ÿ0-9][\w'’.-]*", text))
    lo, hi = arch["words"]
    if words < lo or words > hi:
        lib.warn(where, f"{words} palavras (faixa esperada {lo}-{hi})")

    last = next((l.strip() for l in reversed(text.strip().split("\n")) if l.strip()), "")
    if last and not last.startswith(("|", "```")) and not last.endswith(TERMINAL):
        truncated = any(c.get("kind") == "truncated" for c in cav)
        msg = f"termina sem pontuação final, parece truncado: '…{last[-40:]}'"
        (lib.warn if truncated else lib.err)(where, msg + (" (já registrado como truncated)" if truncated else ""))

    if tax["archetype"] == "messaging":
        m = re.search(r"^## Representative Evidence\s*$(.*?)(?=^## |\Z)", body, re.M | re.S | re.I)
        if m and not re.search(r"[\"“]", m.group(1)):
            lib.warn(where, "Representative Evidence sem citações literais entre aspas")
    marks = len(re.findall(r"\(extrapolated", body, re.I))
    if status == "limited" and marks == 0:
        lib.warn(where, "limited sem nenhuma marcação (Extrapolated): marque as afirmações inferidas")
    if status == "sufficient" and marks > 6:
        lib.warn(where, f"{marks} marcações (Extrapolated) num documento sufficient: considere limited")


def check_links(lib, rel, content):
    for target in re.findall(r"\]\(([^)\s]+)\)", content):
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        path = os.path.normpath(os.path.join(lib.root, posixpath.dirname(rel), target.split("#")[0]))
        if not os.path.exists(path):
            lib.err(rel, f"link quebrado: {target}")


def cmd_check(a):
    lib = Library(a.library)
    m = lib.manifest
    for k in ("product", "source", "generator", "generated", "language", "categories"):
        if k not in m:
            lib.err("manifest.json", f"campo '{k}' ausente")
    if not str(m.get("lede", "")).strip():
        lib.err("manifest.json", "lede vazio: escreva uma frase (pt-BR) descrevendo o produto")
    listed = {c["id"] for c in lib.cats} | {p["id"] for p in lib.pending}
    for cid in TAX_CATS:
        if cid not in listed:
            lib.err("manifest.json", f"categoria '{cid}' não está em categories nem em pending")
    for c in lib.cats:
        tax = TAX_CATS.get(c["id"])
        if not tax:
            lib.warn("manifest.json", f"categoria fora da taxonomia: '{c['id']}'")
            continue
        have = {d["id"] for d in lib.docs_in(c["id"])}
        for x in tax["docs"]:
            if x["id"] not in have:
                lib.err(f"{c['id']}/", f"documento obrigatório ausente: {x['id']}.md")
        if tax.get("dynamic") and not have:
            lib.err(f"{c['id']}/", "nenhuma funcionalidade documentada (use init --feature)")
        if not tax.get("dynamic"):
            for extra in sorted(have - {x["id"] for x in tax["docs"]}):
                lib.warn(f"{c['id']}/{extra}.md", "documento fora da taxonomia")
    for d in lib.docs:
        check_doc(lib, d)
    for rel, content in lib.plan().items():
        p = lib.root / rel
        if not p.exists():
            lib.err(rel, "arquivo gerado ausente: rode `build`")
        elif p.read_text(encoding="utf-8") != content:
            lib.err(rel, "desatualizado em relação ao frontmatter/corpo: rode `build`")
        check_links(lib, rel, content)
    report(lib)
    failed = lib.errors or (a.strict and lib.warnings)
    raise SystemExit(1 if failed else 0)


def report(lib):
    for where, msg in sorted(lib.errors):
        print(f"ERRO  {where}: {msg}")
    for where, msg in sorted(lib.warnings):
        print(f"AVISO {where}: {msg}")
    print(f"\n{len(lib.errors)} erro(s), {len(lib.warnings)} aviso(s) em {len(lib.docs)} documento(s).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init", help="cria a biblioteca e os stubs dos documentos")
    i.add_argument("url", metavar="fonte", help="URL do site, ou caminho de um documento interno (modo documento interno)")
    i.add_argument("--product", help="nome do produto como a empresa escreve")
    i.add_argument("--slug", help="nome da pasta (padrão: primeiro rótulo do domínio)")
    i.add_argument("--root", default="vicaura", help="pasta raiz das bibliotecas (padrão: vicaura)")
    i.add_argument("--feature", action="append", help="nome de uma funcionalidade (repita a opção)")
    i.add_argument("--skip", action="append", help="id de categoria a deixar como pendente (repita a opção)")
    i.add_argument("--generator", default="wonderlust")
    i.add_argument("--date", help="data de geração AAAA-MM-DD (padrão: hoje, UTC)")
    i.add_argument("--lede", help="frase (pt-BR) que descreve o produto")
    i.add_argument("--own-product", action="store_true",
                   help="a biblioteca descreve o nosso próprio produto (muda o aviso do README)")
    b = sub.add_parser("build", help="regenera cabeçalhos, READMEs e manifest.json")
    b.add_argument("library")
    c = sub.add_parser("check", help="valida estrutura, frontmatter e consistência")
    c.add_argument("library")
    c.add_argument("--strict", action="store_true", help="avisos também falham")
    a = ap.parse_args()
    {"init": cmd_init, "build": cmd_build, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    main()
