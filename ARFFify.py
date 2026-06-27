import streamlit as st
import pandas as pd
import re

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ARFFify",
    page_icon="🤖",
    layout="centered",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Header ── */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.15rem;
        line-height: 1.2;
    }
    .arff { color: #000000; }
    .ify  { color: #1a73e8; }
    .subtitle {
        color: #555;
        font-size: 0.95rem;
        margin-bottom: 0.9rem;
    }
    .tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-bottom: 0.4rem;
    }
    .domain-tag {
        background: #e8f0fe;
        color: #1a73e8;
        font-size: 0.71rem;
        font-weight: 600;
        border-radius: 20px;
        padding: 0.18rem 0.6rem;
        letter-spacing: 0.3px;
    }

    /* ── Step cards ── */
    .step-card {
        background: #f8f9fa;
        border-left: 4px solid #1a73e8;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.9rem;
    }
    .step-label {
        font-weight: 700;
        color: #1a73e8;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin: 0;
    }
    .step-desc {
        color: #555;
        font-size: 0.82rem;
        margin-top: 0.15rem;
    }

    /* ── Info / success / warn boxes ── */
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #1565c0;
        border-radius: 6px;
        padding: 0.7rem 1rem;
        font-size: 0.86rem;
        color: #0d2a5c;
        margin-bottom: 0.75rem;
    }
    .success-box {
        background: #e8f5e9;
        border-left: 4px solid #2e7d32;
        border-radius: 6px;
        padding: 0.8rem 1rem;
        font-size: 0.9rem;
    }
    .warn-box {
        background: #fff8e1;
        border-left: 4px solid #f9a825;
        border-radius: 6px;
        padding: 0.7rem 1rem;
        font-size: 0.86rem;
    }

    /* ── Column select grid ── */
    .col-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 0.4rem;
        margin-top: 0.5rem;
    }

    /* ── Type badge pills ── */
    .badge-numeric {
        background: #e8f5e9; color: #2e7d32;
        font-size: 0.68rem; font-weight: 700;
        border-radius: 4px; padding: 1px 6px;
        margin-left: 4px; vertical-align: middle;
    }
    .badge-nominal {
        background: #fff3e0; color: #e65100;
        font-size: 0.68rem; font-weight: 700;
        border-radius: 4px; padding: 1px 6px;
        margin-left: 4px; vertical-align: middle;
    }
    .badge-string {
        background: #f3e5f5; color: #7b1fa2;
        font-size: 0.68rem; font-weight: 700;
        border-radius: 4px; padding: 1px 6px;
        margin-left: 4px; vertical-align: middle;
    }

    /* ── Footer ── */
    .footer-bar {
        background: linear-gradient(90deg, #0d1b2a 0%, #1a3a5c 100%);
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-top: 1.5rem;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
    }
    .footer-brand { font-size: 1.15rem; font-weight: 800; color: #fff; letter-spacing: 0.5px; }
    .footer-brand span { color: #4da6ff; }
    .footer-meta { font-size: 0.78rem; color: #a0b8cc; text-align: right; line-height: 1.6; }
    .footer-meta a { color: #4da6ff; text-decoration: none; font-weight: 600; }
    .footer-meta a:hover { text-decoration: underline; }
    .footer-stack { font-size: 0.72rem; color: #6a8a9e; margin-top: 0.15rem; }
    .footer-copy  { font-size: 0.70rem; color: #4a6a7e; margin-top: 0.1rem; }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-title">🤖 <span class="arff">ARFF</span><span class="ify">ify</span></div>
<div class="subtitle">A Weka-compatible ARFF Converter — works across all domains</div>
<div class="tag-row">
  <span class="domain-tag">⚡ EEE</span>
  <span class="domain-tag">💻 CSE</span>
  <span class="domain-tag">🧪 Chemistry</span>
  <span class="domain-tag">📊 Statistics</span>
  <span class="domain-tag">🌾 Agriculture</span>
  <span class="domain-tag">🏥 Medicine</span>
  <span class="domain-tag">📐 Engineering</span>
  <span class="domain-tag">🌍 Any Domain</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Helpers ───────────────────────────────────────────────────────────────────
def infer_arff_type(series: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(series):
        return "NUMERIC"
    return "NOMINAL"

def safe_arff_name(name: str) -> str:
    if re.search(r'[\s,{}\'"\\%@]', str(name)):
        return f'"{name}"'
    return str(name)

def build_arff(df: pd.DataFrame, relation: str, attr_types: dict,
               class_col: str, class_map: dict | None) -> str:
    lines = [f"@relation {safe_arff_name(relation)}", ""]
    feature_cols = [c for c in df.columns if c != class_col]

    for col in feature_cols:
        atype = attr_types.get(col, "NUMERIC")
        aname = safe_arff_name(col)
        if atype == "NUMERIC":
            lines.append(f"@attribute {aname} NUMERIC")
        elif atype == "STRING":
            lines.append(f"@attribute {aname} STRING")
        else:
            vals = sorted(df[col].dropna().astype(str).unique().tolist())
            lines.append(f"@attribute {aname} " + "{" + ", ".join(vals) + "}")

    # Apply class map before computing values
    df_out = df.copy()
    if class_map:
        df_out[class_col] = df_out[class_col].map(class_map).fillna(df_out[class_col].astype(str))

    class_vals = sorted(df_out[class_col].astype(str).unique().tolist())
    lines.append(f"@attribute class " + "{" + ", ".join(class_vals) + "}")
    lines += ["", "@data"]

    for _, row in df_out.iterrows():
        parts = []
        for col in feature_cols:
            val = row[col]
            parts.append("?" if pd.isna(val) else str(val))
        parts.append(str(row[class_col]))
        lines.append(",".join(parts))

    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 · Upload CSV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label">Step 1 · Upload your CSV dataset</div>
  <div class="step-desc">Any CSV with a header row — no special column names required</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"],
    help="Accepts any CSV with a header row. Works for EEE, CSE, Chemistry, Agriculture, Medicine, Stats — any domain."
)

df_raw = None
if uploaded_file:
    try:
        df_raw = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded **{len(df_raw):,}** rows × **{len(df_raw.columns)}** columns")
        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("🔍 Preview first 5 rows"):
                st.dataframe(df_raw.head(), use_container_width=True)
        with col_b:
            with st.expander("📋 Column summary"):
                summary = pd.DataFrame({
                    "Column": df_raw.columns,
                    "Type": df_raw.dtypes.astype(str).values,
                    "Non-null": df_raw.notna().sum().values,
                    "Unique": df_raw.nunique().values,
                })
                st.dataframe(summary, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Could not read file: {e}")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 · Select columns to keep
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label">Step 2 · Select columns to keep</div>
  <div class="step-desc">Deselect ID columns, free-text fields, or any irrelevant features</div>
</div>
""", unsafe_allow_html=True)

df_input = None
selected_cols = []

if df_raw is not None:
    st.markdown("""
    <div class="info-box">
      💡 <b>Tip:</b> Exclude ID / index columns (e.g. <code>PatientID</code>, <code>SampleNo</code>) —
      they have no predictive value in Weka and will inflate your attribute list.
    </div>
    """, unsafe_allow_html=True)

    all_cols = list(df_raw.columns)

    # Smart defaults: pre-deselect obvious ID/index columns
    id_patterns = re.compile(r'(^id$|_id$|^index$|^no\.?$|^sr\.?$|^s\.?no|^serial)', re.IGNORECASE)
    default_selected = [c for c in all_cols if not id_patterns.search(c)]

    selected_cols = st.multiselect(
        f"Choose columns to include ({len(all_cols)} available)",
        options=all_cols,
        default=default_selected,
        help="All columns are selected by default. Remove any you don't want in the ARFF."
    )

    if len(selected_cols) < 2:
        st.markdown('<div class="warn-box">⚠️ Select at least 2 columns (1 feature + 1 class).</div>', unsafe_allow_html=True)
    else:
        df_input = df_raw[selected_cols].copy()
        st.success(f"✅ **{len(selected_cols)}** columns selected · **{len(df_input):,}** rows retained")
else:
    st.info("Upload a CSV in Step 1 first.")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 · @relation name
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label">Step 3 · Set ARFF @relation name</div>
  <div class="step-desc">The dataset identifier that appears at the top of the ARFF file</div>
</div>
""", unsafe_allow_html=True)

relation_name = st.text_input(
    "@relation name",
    placeholder="e.g.  heart_disease   |   soil_nutrients   |   fault_detection",
    help="Avoid spaces — use underscores. This is how Weka identifies your dataset."
)
if relation_name.strip():
    st.code(f"@relation {relation_name.strip()}", language="text")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 · Class / target column
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label">Step 4 · Select class / target column</div>
  <div class="step-desc">The column Weka will learn to predict — becomes <code>@attribute class</code></div>
</div>
""", unsafe_allow_html=True)

class_col = None
if df_input is not None and len(selected_cols) >= 2:
    class_col = st.selectbox(
        "Class / target column",
        options=selected_cols,
        index=len(selected_cols) - 1,
        help="Usually the last column. In Weka this is always placed last in ARFF."
    )
    if class_col:
        unique_classes = df_input[class_col].dropna().unique().tolist()
        n_unique = len(unique_classes)
        display_vals = unique_classes[:10]
        suffix = f" … (+{n_unique - 10} more)" if n_unique > 10 else ""
        st.markdown(f"**Detected {n_unique} class value(s):** `{display_vals}`{suffix}")
else:
    st.info("Complete Steps 1 & 2 first.")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 · Class label mapping
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label">Step 5 · Class label mapping <span style="font-weight:400;color:#888;font-size:0.78rem;text-transform:none;letter-spacing:0">(optional)</span></div>
  <div class="step-desc">Rename raw class values to meaningful labels before writing ARFF</div>
</div>
""", unsafe_allow_html=True)

class_map = None
if df_input is not None and class_col:
    unique_classes = df_input[class_col].dropna().unique().tolist()
    use_map = st.checkbox(
        "Rename class values",
        value=False,
        help="e.g. map 1 → active, 0 → inactive  |  0 → Fault, 1 → Normal  |  1 → Diseased, 0 → Healthy"
    )
    if use_map:
        st.markdown("Enter a new label for each detected value:")
        n = len(unique_classes)
        map_cols = st.columns(min(n, 4))
        class_map = {}
        for i, val in enumerate(unique_classes):
            with map_cols[i % 4]:
                new_label = st.text_input(
                    f"`{val}` →",
                    value=str(val),
                    key=f"clsmap_{i}",
                    placeholder="new label"
                )
                class_map[val] = new_label.strip() if new_label.strip() else str(val)

        if class_map:
            preview_str = "  ·  ".join(f"`{k}` → `{v}`" for k, v in class_map.items())
            st.markdown(f"**Mapping preview:** {preview_str}")
else:
    st.info("Complete Steps 1–4 first.")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 · Attribute types
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label">Step 6 · Attribute types <span style="font-weight:400;color:#888;font-size:0.78rem;text-transform:none;letter-spacing:0">(auto-detected, override if needed)</span></div>
  <div class="step-desc">
    <b>NUMERIC</b> — continuous numbers &nbsp;·&nbsp;
    <b>NOMINAL</b> — categories / labels &nbsp;·&nbsp;
    <b>STRING</b> — free text
  </div>
</div>
""", unsafe_allow_html=True)

attr_types = {}
if df_input is not None and class_col:
    feature_cols = [c for c in df_input.columns if c != class_col]

    if not feature_cols:
        st.warning("No feature columns left after removing the class column.")
    else:
        # Count auto-detected types for summary line
        n_numeric = sum(1 for c in feature_cols if infer_arff_type(df_input[c]) == "NUMERIC")
        n_nominal = len(feature_cols) - n_numeric

        st.markdown(
            f"<div class='info-box'>🔍 Auto-detected: "
            f"<b>{n_numeric} NUMERIC</b> and <b>{n_nominal} NOMINAL</b> across {len(feature_cols)} feature columns. "
            f"Override any below if the auto-detection is wrong.</div>",
            unsafe_allow_html=True
        )

        n_cols_grid = 3
        rows = [feature_cols[i:i+n_cols_grid] for i in range(0, len(feature_cols), n_cols_grid)]
        for row_group in rows:
            cols = st.columns(n_cols_grid)
            for j, col_name in enumerate(row_group):
                inferred = infer_arff_type(df_input[col_name])
                with cols[j]:
                    chosen = st.selectbox(
                        col_name,
                        options=["NUMERIC", "NOMINAL", "STRING"],
                        index=["NUMERIC", "NOMINAL", "STRING"].index(inferred),
                        key=f"atype_{col_name}",
                    )
                    attr_types[col_name] = chosen
else:
    st.info("Complete Steps 1–4 first.")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE
# ══════════════════════════════════════════════════════════════════════════════
ready = (
    df_input is not None
    and len(selected_cols) >= 2
    and bool(relation_name.strip())
    and class_col is not None
    and bool(attr_types)
)

if not ready:
    missing = []
    if df_input is None: missing.append("upload a CSV (Step 1)")
    elif len(selected_cols) < 2: missing.append("select ≥2 columns (Step 2)")
    if not relation_name.strip(): missing.append("set a relation name (Step 3)")
    if not class_col: missing.append("choose a class column (Step 4)")
    if missing:
        st.info("⬆️  Still needed: " + " · ".join(missing))

generate_btn = st.button(
    "⚙️  Generate ARFF File",
    disabled=not ready,
    use_container_width=True,
    type="primary",
)

if generate_btn and ready:
    try:
        with st.status("Building ARFF…", expanded=True) as status:
            st.write("🗂️  Preparing data…")
            effective_map = (
                class_map
                if class_map and any(str(k) != str(v) for k, v in class_map.items())
                else None
            )
            st.write("📝  Writing ARFF attributes and data…")
            arff_content = build_arff(
                df=df_input,
                relation=relation_name.strip(),
                attr_types=attr_types,
                class_col=class_col,
                class_map=effective_map,
            )
            status.update(label="✅ ARFF ready!", state="complete", expanded=False)

        arff_lines = arff_content.split("\n")
        feature_cols = [c for c in df_input.columns if c != class_col]
        numeric_count = sum(1 for c in feature_cols if attr_types.get(c, "NUMERIC") == "NUMERIC")
        nominal_count = sum(1 for c in feature_cols if attr_types.get(c, "NUMERIC") == "NOMINAL")

        st.markdown("---")
        st.markdown("### 📋 Results Summary")

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Instances", f"{len(df_input):,}")
        c2.metric("Attributes", f"{len(feature_cols)}")
        c3.metric("Numeric", f"{numeric_count}")
        c4.metric("Nominal", f"{nominal_count}")

        # Class value count after mapping
        df_preview = df_input.copy()
        if effective_map:
            df_preview[class_col] = df_preview[class_col].map(effective_map).fillna(df_preview[class_col].astype(str))
        c5.metric("Classes", f"{df_preview[class_col].nunique()}")

        with st.expander("👁️  Preview ARFF (first 40 lines)"):
            st.code("\n".join(arff_lines[:40]), language="text")

        arff_bytes = arff_content.encode("utf-8")
        filename = f"{relation_name.strip().replace(' ', '_')}.arff"

        st.download_button(
            label="⬇️  Download ARFF File",
            data=arff_bytes,
            file_name=filename,
            mime="text/plain",
            use_container_width=True,
            type="primary",
        )

        st.markdown(
            f'<div class="success-box">🎉 <b>{filename}</b> is ready — '
            f'{len(arff_bytes)/1024:.1f} KB &nbsp;·&nbsp; '
            f'{len(df_input):,} instances &nbsp;·&nbsp; '
            f'{len(feature_cols)} attributes</div>',
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"❌ Failed to generate ARFF: {e}")

# ─── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div class="footer-bar">
    <div class="footer-brand">🤖 ARFF<span>ify</span></div>
    <div class="footer-meta">
        Designed &amp; developed by <a href="https://www.linkedin.com/in/nabiulorko" target="_blank">Nabiul Orko</a><br>
        <span class="footer-stack">Python · Pandas · Streamlit · Weka ARFF</span><br>
        <span class="footer-copy">© 2026 All Rights Reserved</span>
    </div>
</div>
""", unsafe_allow_html=True)
