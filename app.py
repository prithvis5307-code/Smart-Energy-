import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="ElectroSight | Campus Energy Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling (Dark Navy, Electric Teal, Slate Gray, Clean KPI Cards)
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary-navy: #0A192F;
    --navy-card: #112240;
    --navy-surface: #1E3A8A;
    --accent-teal: #00F0FF;
    --teal-glow: rgba(0, 240, 255, 0.15);
    --teal-dark: #0D9488;
    --accent-emerald: #10B981;
    --accent-amber: #F59E0B;
    --accent-rose: #F43F5E;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --card-shadow: 0 10px 25px -5px rgba(2, 6, 23, 0.4), 0 8px 10px -6px rgba(2, 6, 23, 0.3);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top right, #0F172A 0%, #080D1A 100%);
    color: var(--text-primary);
}

section[data-testid="stSidebar"] {
    background-color: #060B14 !important;
    border-right: 1px solid var(--border-subtle);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

.kpi-card {
    background: linear-gradient(135deg, rgba(17, 34, 64, 0.85) 0%, rgba(10, 25, 47, 0.95) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    box-shadow: var(--card-shadow);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 240, 255, 0.3);
    box-shadow: 0 12px 30px -5px rgba(0, 240, 255, 0.12);
}

.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00F0FF, #3B82F6);
    opacity: 0.9;
}

.kpi-title {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.kpi-value {
    font-size: 1.85rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.kpi-sub {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.35rem;
}

.page-header-box {
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.25) 0%, rgba(15, 23, 42, 0.6) 100%);
    border: 1px solid rgba(0, 240, 255, 0.2);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    backdrop-filter: blur(8px);
}

.page-header-title {
    font-size: 2.1rem;
    font-weight: 800;
    background: linear-gradient(90deg, #FFFFFF 30%, #38BDF8 70%, #00F0FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -0.03em;
}

.page-header-desc {
    color: #94A3B8;
    font-size: 0.95rem;
    margin-top: 0.4rem;
    margin-bottom: 0;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: -0.01em;
    margin-top: 1.2rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-title span.badge {
    background: rgba(0, 240, 255, 0.1);
    color: #00F0FF;
    border: 1px solid rgba(0, 240, 255, 0.3);
    font-size: 0.7rem;
    padding: 0.15rem 0.5rem;
    border-radius: 9999px;
    font-weight: 600;
}

.info-banner {
    background: rgba(15, 23, 42, 0.7);
    border-left: 4px solid var(--accent-teal);
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    font-size: 0.9rem;
    color: #CBD5E1;
    margin-bottom: 1.2rem;
}

.rec-card {
    background: rgba(17, 34, 64, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.9rem;
    transition: border-color 0.2s ease;
}
.rec-card:hover {
    border-color: rgba(0, 240, 255, 0.3);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 4px;
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    border-radius: 8px 8px 0 0;
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 0.9rem;
    border: none;
    padding: 0 16px;
    background: transparent;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    color: #00F0FF !important;
    background: rgba(0, 240, 255, 0.08) !important;
    border-bottom: 2px solid #00F0FF !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    overflow: hidden;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

PLOTLY_LAYOUT_DEFAULTS = dict(
    paper_bgcolor='rgba(10, 25, 47, 0.4)',
    plot_bgcolor='rgba(10, 25, 47, 0.2)',
    font=dict(family='Plus Jakarta Sans, sans-serif', color='#94A3B8', size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(
        gridcolor='rgba(255, 255, 255, 0.06)',
        zerolinecolor='rgba(255, 255, 255, 0.1)',
        tickfont=dict(color='#94A3B8')
    ),
    yaxis=dict(
        gridcolor='rgba(255, 255, 255, 0.06)',
        zerolinecolor='rgba(255, 255, 255, 0.1)',
        tickfont=dict(color='#94A3B8')
    ),
    legend=dict(
        bgcolor='rgba(15, 23, 42, 0.8)',
        bordercolor='rgba(255, 255, 255, 0.1)',
        borderwidth=1,
        font=dict(color='#E2E8F0')
    ),
    hoverlabel=dict(
        bgcolor='#0F172A',
        font_size=12,
        font_family='Plus Jakarta Sans, sans-serif',
        bordercolor='#00F0FF'
    )
)

def apply_chart_theme(fig, height=380, title=None):
    fig.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
    fig.update_layout(height=height)
    if title:
        fig.update_layout(title=dict(text=title, font=dict(color='#F8FAFC', size=14, weight=600)))
    return fig

BUILDINGS = ["Academic","Boys_main","Boys_backup","Facilities","Girls_main","Girls_backup","Lecture","Library","Mess"]
BUILDING_LABELS = {
    "Academic": "Academic Building",
    "Boys_main": "Boys Dorm Main",
    "Boys_backup": "Boys Dorm UPS",
    "Facilities": "Facilities Center",
    "Girls_main": "Girls Dorm Main",
    "Girls_backup": "Girls Dorm UPS",
    "Lecture": "Lecture Hall",
    "Library": "Central Library",
    "Mess": "Dining Mess"
}
COLOR_PALETTE = ["#00F0FF", "#38BDF8", "#3B82F6", "#6366F1", "#8B5CF6", "#EC4899", "#10B981", "#F59E0B", "#F97316"]

def friendly(col): return BUILDING_LABELS.get(col, col)
def fmt_kw(v): return "{:,.1f} kW".format(v)
def fmt_kwh(v): return "{:,.0f} kWh".format(v)

def render_kpi(icon, title, value, subtext, border_accent=None):
    accent_style = f"border-top: 3px solid {border_accent};" if border_accent else ""
    st.markdown(f"""
        <div class="kpi-card" style="{accent_style}">
            <div class="kpi-title">{icon} {title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{subtext}</div>
        </div>
    """, unsafe_allow_html=True)

@st.cache_data(show_spinner="Loading dataset...")
def load_data():
    df = pd.read_csv("dataset/allpower.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["hour"] = df["timestamp"].dt.hour
    df["date"] = df["timestamp"].dt.date
    df["month"] = df["timestamp"].dt.month
    df["year"] = df["timestamp"].dt.year
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["total_power_W"] = df[BUILDINGS].sum(axis=1, min_count=1)
    df["energy_kwh"] = df["total_power_W"] / 1000 / 60
    return df

@st.cache_data(show_spinner="Computing daily summaries...")
def compute_daily(_df):
    daily_energy = _df.groupby("date")["energy_kwh"].sum()
    daily_energy.index = pd.to_datetime(daily_energy.index)
    building_daily = _df.groupby("date")[BUILDINGS].sum() / 1000 / 60
    building_daily.index = pd.to_datetime(building_daily.index)
    Q1 = daily_energy.quantile(0.25)
    Q3 = daily_energy.quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR
    anomalies = daily_energy[(daily_energy > upper) | (daily_energy < lower)]
    return daily_energy, building_daily, anomalies, upper, lower

@st.cache_data(show_spinner="Computing hourly patterns...")
def compute_hourly(_df):
    return _df.groupby("hour")["total_power_W"].mean() / 1000

@st.cache_data
def compute_monthly(daily_energy):
    return daily_energy.resample("ME").sum()

df = load_data()
daily_energy, building_daily, anomalies, upper_limit, lower_limit = compute_daily(df)
hourly_kw = compute_hourly(df)
monthly_energy = compute_monthly(daily_energy)
avg_daily = daily_energy.mean()
peak_power_kw = df["total_power_W"].max() / 1000
highest_bldg = df[BUILDINGS].mean().idxmax()
anomaly_count = len(anomalies)

with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.8rem;">
            <div style="background: linear-gradient(135deg, #00F0FF, #3B82F6); padding: 9px; border-radius: 12px; display:flex; align-items:center; justify-content:center; box-shadow: 0 4px 15px rgba(0, 240, 255, 0.4);">
                <span style="font-size: 1.4rem;">⚡</span>
            </div>
            <div>
                <h2 style="font-size:1.25rem; font-weight:800; color:#FFFFFF; margin:0; line-height:1.1; letter-spacing:-0.02em;">ElectroSight</h2>
                <span style="font-size:0.72rem; color:#00F0FF; text-transform:uppercase; font-weight:700; letter-spacing:0.08em;">Campus Power Intel</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.82rem; color:#94A3B8; margin-bottom:1.2rem; line-height:1.4;'>Automated electricity consumption diagnostics & telemetry analytics platform.</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<p style='font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; font-weight:700; margin-bottom:0.4rem;'>Navigation</p>", unsafe_allow_html=True)
    PAGES = ["Dashboard", "Consumption Analysis", "Anomaly Detection", "Recommendations", "Data Quality"]
    page = st.radio("Navigate to", PAGES, label_visibility="collapsed")
    st.divider()

    st.markdown("""
        <div style="background: rgba(17, 34, 64, 0.6); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 0.9rem; font-size: 0.78rem;">
            <div style="color:#00F0FF; font-weight:700; margin-bottom:0.4rem;">METRIC COVERAGE</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem; color:#94A3B8;"><span>Telemetry:</span> <b style="color:#F8FAFC;">2.31M rows</b></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem; color:#94A3B8;"><span>Interval:</span> <b style="color:#F8FAFC;">60 seconds</b></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem; color:#94A3B8;"><span>Buildings:</span> <b style="color:#F8FAFC;">9 meters</b></div>
            <div style="display:flex; justify-content:space-between; color:#94A3B8;"><span>Period:</span> <b style="color:#F8FAFC;">2013 – 2017</b></div>
        </div>
    """, unsafe_allow_html=True)

# ======================== DASHBOARD ========================
if page == "Dashboard":
    st.markdown("""
        <div class="page-header-box">
            <h1 class="page-header-title">Executive Energy Dashboard</h1>
            <p class="page-header-desc">High-level telemetry overview, campus load distribution, and daily aggregate anomalies across 9 buildings.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("📅", "Avg Daily Energy", fmt_kwh(avg_daily), "Mean daily consumption baseline", "#00F0FF")
    with c2:
        render_kpi("⚡", "Peak Power Draw", fmt_kw(peak_power_kw), "Historical maximum instantaneous load", "#38BDF8")
    with c3:
        render_kpi("🏆", "Dominant Facility", friendly(highest_bldg), "Highest continuous consumer", "#F59E0B")
    with c4:
        render_kpi("🚨", "Anomalous Days", f"{anomaly_count} Days", "Identified via 1.5×IQR boundaries", "#F43F5E")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="section-title">
            <span>Daily Campus Energy Baseline & Anomaly Overlay</span>
            <span class="badge">Historical Chronology</span>
        </div>
    """, unsafe_allow_html=True)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=daily_energy.index,
        y=daily_energy.values,
        mode="lines",
        name="Daily Energy",
        line=dict(color="#00F0FF", width=1.5),
        hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Energy:</b> %{y:,.0f} kWh<extra></extra>"
    ))
    fig_trend.add_hline(
        y=avg_daily,
        line_dash="dash",
        line_color="#F59E0B",
        annotation_text=f"Campus Average: {avg_daily:,.0f} kWh",
        annotation_position="top left",
        annotation_font=dict(color="#F59E0B", size=11)
    )
    fig_trend.add_trace(go.Scatter(
        x=anomalies.index,
        y=anomalies.values,
        mode="markers",
        name="Anomaly Event",
        marker=dict(color="#F43F5E", size=7, symbol="diamond", line=dict(width=1, color="#FFFFFF")),
        hovertemplate="<b>🚨 Anomaly:</b> %{x|%Y-%m-%d}<br><b>Energy:</b> %{y:,.0f} kWh<extra></extra>"
    ))
    apply_chart_theme(fig_trend, height=380)
    fig_trend.update_layout(yaxis_title="Energy (kWh)", xaxis_title="Timestamp")
    st.plotly_chart(fig_trend, width="stretch")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
            <div class="section-title">
                <span>Diurnal Profile (Hourly Average)</span>
                <span class="badge">24-Hr Cycle</span>
            </div>
        """, unsafe_allow_html=True)
        fig_hour = px.bar(
            x=hourly_kw.index,
            y=hourly_kw.values,
            labels={"x": "Hour of Day (0-23)", "y": "Avg Power (kW)"},
            color=hourly_kw.values,
            color_continuous_scale=[[0, "#0A2540"], [0.5, "#0D9488"], [1, "#00F0FF"]],
        )
        fig_hour.update_traces(
            marker_line_width=0,
            hovertemplate="<b>Hour:</b> %{x}:00<br><b>Power:</b> %{y:,.1f} kW<extra></extra>"
        )
        fig_hour.update_coloraxes(showscale=False)
        apply_chart_theme(fig_hour, height=320)
        fig_hour.update_xaxes(tickmode='linear', tick0=0, dtick=2)
        st.plotly_chart(fig_hour, width="stretch")

    with col_r:
        st.markdown("""
            <div class="section-title">
                <span>Mean Power Demand by Facility</span>
                <span class="badge">Facility Breakdown</span>
            </div>
        """, unsafe_allow_html=True)
        avg_bldg = (df[BUILDINGS].mean().sort_values(ascending=True) / 1000)
        fig_bldg = px.bar(
            x=avg_bldg.values,
            y=[friendly(c) for c in avg_bldg.index],
            orientation="h",
            labels={"x": "Average Demand (kW)", "y": ""},
            color=avg_bldg.values,
            color_continuous_scale=[[0, "#1E3A8A"], [1, "#38BDF8"]],
        )
        fig_bldg.update_traces(
            marker_line_width=0,
            hovertemplate="<b>Building:</b> %{y}<br><b>Demand:</b> %{x:,.1f} kW<extra></extra>"
        )
        fig_bldg.update_coloraxes(showscale=False)
        apply_chart_theme(fig_bldg, height=320)
        st.plotly_chart(fig_bldg, width="stretch")

# ======================== CONSUMPTION ANALYSIS ========================
elif page == "Consumption Analysis":
    st.markdown("""
        <div class="page-header-box">
            <h1 class="page-header-title">Deep Dive: Consumption Analysis</h1>
            <p class="page-header-desc">Granular examination of power load distributions across facilities, temporal diurnal heatmaps, and long-term energy consumption trends.</p>
        </div>
    """, unsafe_allow_html=True)

    years = sorted(df["year"].unique())
    col_filter, _ = st.columns([2, 1])
    with col_filter:
        sel_years = st.multiselect("Active Analytical Years", years, default=years, help="Filter telemetry dataset by selected recording periods")
    if not sel_years:
        st.warning("Select at least one observation year to populate the analytics views.")
        st.stop()

    df_f = df[df["year"].isin(sel_years)]
    de_filtered = daily_energy[daily_energy.index.year.isin(sel_years)]
    me_filtered = de_filtered.resample("ME").sum()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 Building Distribution",
        "🕐 Diurnal & Temporal Patterns",
        "📅 Daily Energy Timeline",
        "📆 Monthly Aggregations"
    ])

    with tab1:
        st.markdown("<div class='section-title'><span>Comparative Power Consumption by Facility</span></div>", unsafe_allow_html=True)
        col_bar, col_donut = st.columns([1.3, 1])
        avg_b = (df_f[BUILDINGS].mean() / 1000).sort_values(ascending=False)

        with col_bar:
            fig = px.bar(
                x=[friendly(c) for c in avg_b.index],
                y=avg_b.values,
                labels={"x": "Facility", "y": "Mean Power (kW)"},
                color=avg_b.values,
                color_continuous_scale=[[0, "#0E3A5D"], [0.5, "#0D9488"], [1, "#00F0FF"]],
                text=[f"{v:.1f} kW" for v in avg_b.values]
            )
            fig.update_traces(
                textposition='outside',
                textfont=dict(color='#CBD5E1', size=10),
                hovertemplate="<b>%{x}:</b> %{y:.1f} kW<extra></extra>"
            )
            fig.update_coloraxes(showscale=False)
            apply_chart_theme(fig, height=400, title="Average Power Demand (kW)")
            fig.update_xaxes(tickangle=-30)
            st.plotly_chart(fig, width="stretch")

        with col_donut:
            fig_pie = px.pie(
                names=[friendly(c) for c in avg_b.index],
                values=avg_b.values,
                hole=0.55,
                color_discrete_sequence=COLOR_PALETTE
            )
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(size=10),
                marker=dict(line=dict(color='#0A192F', width=2))
            )
            apply_chart_theme(fig_pie, height=400, title="Relative Energy Share (%)")
            fig_pie.update_layout(showlegend=False)
            st.plotly_chart(fig_pie, width="stretch")

    with tab2:
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("<div class='section-title'><span>Diurnal Power Curve (Mean Hourly Demand)</span></div>", unsafe_allow_html=True)
            hourly_f = df_f.groupby("hour")["total_power_W"].mean() / 1000
            fig_h = px.line(
                x=hourly_f.index,
                y=hourly_f.values,
                markers=True,
                labels={"x": "Hour of Day (24-Hour)", "y": "Avg Power (kW)"},
                color_discrete_sequence=["#00F0FF"]
            )
            fig_h.update_traces(
                line=dict(width=2.5),
                marker=dict(size=6, color="#00F0FF", line=dict(width=2, color="#0A192F")),
                hovertemplate="<b>Hour:</b> %{x}:00<br><b>Campus Power:</b> %{y:,.1f} kW<extra></extra>"
            )
            fig_h.update_xaxes(tickvals=list(range(0, 24)))
            apply_chart_theme(fig_h, height=360)
            st.plotly_chart(fig_h, width="stretch")

        with col_h2:
            st.markdown("<div class='section-title'><span>Weekly Diurnal Intensity Heatmap (kW)</span></div>", unsafe_allow_html=True)
            pivot = (df_f.groupby(["day_of_week", "hour"])["total_power_W"].mean().unstack("hour") / 1000)
            dow_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            fig_hm = px.imshow(
                pivot,
                x=list(range(24)),
                y=[dow_labels[i] for i in pivot.index],
                labels={"x": "Hour", "y": "Weekday", "color": "kW"},
                color_continuous_scale=[[0, "#081226"], [0.5, "#1E3A8A"], [0.8, "#0D9488"], [1, "#00F0FF"]],
                aspect="auto"
            )
            apply_chart_theme(fig_hm, height=360)
            st.plotly_chart(fig_hm, width="stretch")

    with tab3:
        st.markdown("<div class='section-title'><span>Daily Consumption & 7-Day Rolling Trend</span></div>", unsafe_allow_html=True)
        rolling = de_filtered.rolling(7).mean()

        fig_daily_trend = go.Figure()
        fig_daily_trend.add_trace(go.Scatter(
            x=de_filtered.index,
            y=de_filtered.values,
            mode='lines',
            name='Daily Total (kWh)',
            line=dict(color='rgba(56, 189, 248, 0.45)', width=1),
            hovertemplate="<b>%{x|%Y-%m-%d}:</b> %{y:,.0f} kWh<extra></extra>"
        ))
        fig_daily_trend.add_trace(go.Scatter(
            x=rolling.index,
            y=rolling.values,
            mode='lines',
            name='7-Day Moving Avg',
            line=dict(color='#00F0FF', width=2.5),
            hovertemplate="<b>7-Day Avg:</b> %{y:,.0f} kWh<extra></extra>"
        ))
        fig_daily_trend.add_hline(
            y=de_filtered.mean(),
            line_dash="dash",
            line_color="#F59E0B",
            annotation_text=f"Period Mean: {de_filtered.mean():,.0f} kWh"
        )
        apply_chart_theme(fig_daily_trend, height=400)
        fig_daily_trend.update_layout(yaxis_title="Energy (kWh)", xaxis_title="Date")
        st.plotly_chart(fig_daily_trend, width="stretch")

    with tab4:
        st.markdown("<div class='section-title'><span>Monthly Energy Aggregates</span></div>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            render_kpi("📊", "Avg Monthly Energy", fmt_kwh(me_filtered.mean()), "Average monthly usage")
        with m2:
            render_kpi("🔥", "Max Monthly Energy", fmt_kwh(me_filtered.max()), f"Peak: {me_filtered.idxmax().strftime('%b %Y')}")
        with m3:
            render_kpi("❄️", "Min Monthly Energy", fmt_kwh(me_filtered.min()), f"Lowest: {me_filtered.idxmin().strftime('%b %Y')}")

        me_df = me_filtered.reset_index()
        me_df.columns = ["Month", "Energy_kWh"]
        me_df["MonthLabel"] = me_df["Month"].dt.strftime("%b %Y")

        fig_m = px.bar(
            me_df,
            x="MonthLabel",
            y="Energy_kWh",
            labels={"MonthLabel": "Month", "Energy_kWh": "Energy (kWh)"},
            color="Energy_kWh",
            color_continuous_scale=[[0, "#112240"], [0.6, "#0284C7"], [1, "#00F0FF"]],
        )
        fig_m.update_traces(hovertemplate="<b>%{x}:</b> %{y:,.0f} kWh<extra></extra>")
        fig_m.update_coloraxes(showscale=False)
        apply_chart_theme(fig_m, height=380)
        fig_m.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_m, width="stretch")

elif page == "Anomaly Detection":
    st.markdown("""
        <div class="page-header-box">
            <h1 class="page-header-title">Anomaly Detection Engine</h1>
            <p class="page-header-desc">Statistical Interquartile Range (IQR) outlier screening, anomalous day drill-downs, and facility variance breakdown.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="info-banner">
            <b>Statistical Boundary Model:</b> Daily campus load is modeled via Non-Parametric IQR.<br>
            Normal Band: <b>[{fmt_kwh(lower_limit)} – {fmt_kwh(upper_limit)}]</b> &nbsp;|&nbsp;
            Days exceeding thresholds are flagged as potential consumption leaks, HVAC over-runs, or metering surges.
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi("🚨", "Identified Anomalous Days", str(anomaly_count), f"{anomaly_count / len(daily_energy) * 100:.2f}% of monitored dates", "#F43F5E")
    with c2:
        render_kpi("📈", "Upper Threshold (Q3 + 1.5×IQR)", fmt_kwh(upper_limit), "Statistical High Cutoff", "#F59E0B")
    with c3:
        render_kpi("📉", "Lower Threshold (Q1 − 1.5×IQR)", fmt_kwh(lower_limit), "Statistical Low Cutoff", "#10B981")

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'><span>Daily Load Anomaly Boundary Classification</span></div>", unsafe_allow_html=True)
    normal_days = daily_energy[~daily_energy.index.isin(anomalies.index)]

    fig_a = go.Figure()
    fig_a.add_trace(go.Scatter(
        x=normal_days.index,
        y=normal_days.values,
        mode="lines",
        name="Normal Operations",
        line=dict(color="#38BDF8", width=1.2),
        opacity=0.75,
        hovertemplate="<b>Normal:</b> %{x|%Y-%m-%d}<br><b>Energy:</b> %{y:,.0f} kWh<extra></extra>"
    ))
    fig_a.add_trace(go.Scatter(
        x=anomalies.index,
        y=anomalies.values,
        mode="markers",
        name="Anomalous Day Event",
        marker=dict(color="#F43F5E", size=8, symbol="diamond", line=dict(width=1.5, color="#FFFFFF")),
        hovertemplate="<b>🚨 Outlier:</b> %{x|%Y-%m-%d}<br><b>Energy:</b> %{y:,.0f} kWh<extra></extra>"
    ))
    fig_a.add_hline(
        y=upper_limit,
        line_dash="dash",
        line_color="#F59E0B",
        annotation_text=f"Upper Boundary ({upper_limit:,.0f} kWh)",
        annotation_position="top right"
    )
    fig_a.add_hline(
        y=lower_limit,
        line_dash="dash",
        line_color="#10B981",
        annotation_text=f"Lower Boundary ({lower_limit:,.0f} kWh)",
        annotation_position="bottom right"
    )
    apply_chart_theme(fig_a, height=400)
    fig_a.update_layout(yaxis_title="Energy (kWh)", xaxis_title="Timeline")
    st.plotly_chart(fig_a, width="stretch")

    anom_mask = building_daily.index.isin(anomalies.index)
    avg_anom = building_daily[anom_mask].mean()
    avg_normal = building_daily[~anom_mask].mean()
    additional = (avg_anom - avg_normal).sort_values(ascending=False)
    pct_inc = ((avg_anom - avg_normal) / avg_normal * 100).sort_values(ascending=False)

    col_tbl, col_chart = st.columns([1, 1.2])

    with col_tbl:
        st.markdown("<div class='section-title'><span>Highest Outlier Days (Ranked)</span></div>", unsafe_allow_html=True)
        anom_df = anomalies.sort_values(ascending=False).reset_index()
        anom_df.columns = ["Date", "Energy (kWh)"]
        anom_df["Energy (kWh)"] = anom_df["Energy (kWh)"].round(1)
        anom_df["Excess vs Baseline (kWh)"] = (anom_df["Energy (kWh)"] - avg_daily).round(1)
        anom_df["Date"] = anom_df["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(anom_df.head(15), width="stretch", height=360, hide_index=True)

    with col_chart:
        st.markdown("<div class='section-title'><span>Additional Energy on Anomalous Days (kWh)</span></div>", unsafe_allow_html=True)
        add_sorted = additional.sort_values(ascending=True)
        fig_add = px.bar(
            x=add_sorted.values,
            y=[friendly(c) for c in add_sorted.index],
            orientation="h",
            labels={"x": "Surge Consumption (kWh)", "y": ""},
            color=add_sorted.values,
            color_continuous_scale=[[0, "#1E293B"], [0.5, "#BE123C"], [1, "#F43F5E"]],
            text=[f"+{v:,.0f} kWh" for v in add_sorted.values]
        )
        fig_add.update_traces(
            textposition='outside',
            textfont=dict(color='#F8FAFC', size=10),
            hovertemplate="<b>Facility:</b> %{y}<br><b>Surge:</b> +%{x:,.1f} kWh<extra></extra>"
        )
        fig_add.update_coloraxes(showscale=False)
        apply_chart_theme(fig_add, height=360)
        st.plotly_chart(fig_add, width="stretch")

    st.markdown("<div class='section-title'><span>Hourly Load Profile: Normal Days vs Anomalous Days</span></div>", unsafe_allow_html=True)
    anom_dates = set(anomalies.index.date)
    df["_is_anomaly"] = df["date"].isin(anom_dates)
    hourly_anom = df[df["_is_anomaly"]].groupby("hour")["total_power_W"].mean() / 1000
    hourly_normal_h = df[~df["_is_anomaly"]].groupby("hour")["total_power_W"].mean() / 1000

    fig_hp = go.Figure()
    fig_hp.add_trace(go.Scatter(
        x=hourly_normal_h.index,
        y=hourly_normal_h.values,
        mode="lines+markers",
        name="Baseline Days",
        line=dict(color="#38BDF8", width=2.5),
        marker=dict(size=6)
    ))
    fig_hp.add_trace(go.Scatter(
        x=hourly_anom.index,
        y=hourly_anom.values,
        mode="lines+markers",
        name="Anomalous Days",
        line=dict(color="#F43F5E", width=2.5),
        marker=dict(size=6, symbol="diamond")
    ))
    apply_chart_theme(fig_hp, height=360)
    fig_hp.update_layout(xaxis_title="Hour of Day", yaxis_title="Average Demand (kW)")
    fig_hp.update_xaxes(tickvals=list(range(24)))
    st.plotly_chart(fig_hp, width="stretch")

# ======================== RECOMMENDATIONS ========================
elif page == "Recommendations":
    st.markdown("""
        <div class="page-header-box">
            <h1 class="page-header-title">Energy Conservation & Efficiency Roadmap</h1>
            <p class="page-header-desc">Actionable optimization directives derived from empirical load profiles, baselines, and diurnal signatures.</p>
        </div>
    """, unsafe_allow_html=True)

    avg_bldg_kw = df[BUILDINGS].mean() / 1000
    peak_hour = hourly_kw.idxmax()
    low_hour = hourly_kw.idxmin()
    top_bldg = avg_bldg_kw.idxmax()
    top_bldg_kw = avg_bldg_kw.max()
    night_mask = hourly_kw.index.isin(list(range(23, 24)) + list(range(0, 6)))
    night_avg = hourly_kw[night_mask].mean()
    day_avg = hourly_kw[~night_mask].mean()
    night_ratio = night_avg / day_avg * 100
    anom_pct = anomaly_count / len(daily_energy) * 100
    anom_mask_b = building_daily.index.isin(anomalies.index)
    avg_anom_b = building_daily[anom_mask_b].mean()
    avg_norm_b = building_daily[~anom_mask_b].mean()
    pct_inc_b = ((avg_anom_b - avg_norm_b) / avg_norm_b * 100).sort_values(ascending=False)
    top_anom_bldg = pct_inc_b.index[0]
    df["_weekend"] = df["day_of_week"] >= 5
    wknd_avg = df[df["_weekend"]]["total_power_W"].mean() / 1000
    wkdy_avg = df[~df["_weekend"]]["total_power_W"].mean() / 1000

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("🌙", "Night/Day Ratio", f"{night_ratio:.1f}%", f"Night base: {fmt_kw(night_avg)}")
    with c2:
        render_kpi("⏰", "Campus Peak Hour", f"{peak_hour:02d}:00", f"Peak power: {fmt_kw(hourly_kw.max())}")
    with c3:
        render_kpi("📅", "Weekend Load", fmt_kw(wknd_avg), f"vs Weekday: {fmt_kw(wkdy_avg)}")
    with c4:
        render_kpi("🎯", "Prime Target", friendly(top_bldg), f"Continuous: {top_bldg_kw:.1f} kW")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'><span>Tailored Engineering Recommendations</span></div>", unsafe_allow_html=True)

    recs = [
        ("🏆", f"Comprehensive HVAC & Sub-System Energy Audit in {friendly(top_bldg)}",
         f"The <b>{friendly(top_bldg)}</b> draws a sustained average of <b>{top_bldg_kw:.1f} kW</b>, making it the dominant load on campus. Implement centralized BMS scheduling, inspect central chiller loops, and audit server room cooling.",
         "High Impact | Low Effort"),
        ("🌙", "Night-Time Baseline Load Curtailment",
         f"Between midnight and 06:00, campus power stays high at <b>{night_avg:.1f} kW</b>—equivalent to <b>{night_ratio:.0f}%</b> of total daytime power ({day_avg:.1f} kW). Install passive infrared (PIR) occupancy sensors and automated contactor shutoffs for unoccupied corridors and classrooms.",
         "High Impact | Fast ROI"),
        ("⏰", f"Load Staggering & Demand Response Near {peak_hour:02d}:00",
         f"Campus peak load spikes up to <b>{hourly_kw.max():.1f} kW</b> at <b>{peak_hour:02d}:00</b>. Shift energy-dense auxiliary loads (pumping stations, laundry units, cafeteria prep appliances) toward off-peak troughs ({low_hour:02d}:00, {hourly_kw.min():.1f} kW) to reduce maximum demand tariffs.",
         "Tariff Optimization"),
        ("🚨", "Real-Time Anomaly Alerting & Threshold Triggers",
         f"Empirical analysis detected <b>{anomaly_count} days</b> ({anom_pct:.1f}% of total) with severe consumption excursions. <b>{friendly(top_anom_bldg)}</b> exhibited a surge of <b>+{pct_inc_b.iloc[0]:.1f}%</b> above nominal during outliers. Install IoT telemetry triggers to dispatch facilities personnel immediately.",
         "Fault Detection"),
        ("📅", "Weekend Energy Setback Schedules",
         f"Weekend baseline averages <b>{wknd_avg:.1f} kW</b> compared to <b>{wkdy_avg:.1f} kW</b> on weekdays. " +
         ("High weekend idling detected; configure deep setback schedules on building automation controllers for vacant academic spaces." if wknd_avg > 0.75 * wkdy_avg else "Weekend load reductions demonstrate disciplined operational practices; maintain existing procedures."),
         "Policy Optimization"),
        ("🔢", "UPS & Critical Backup Circuit Metrology Enhancement",
         "The UPS metering channels for Boys & Girls Dormitories exhibit notable telemetry gaps. Upgrade current transducers and verify CT calibration to eliminate battery bank parasitic charging losses.",
         "Metrology & Safety"),
        ("☀️", "Rooftop Solar Photovoltaic (PV) Integration",
         f"Campus maintains a consistent daytime base load of ~<b>{day_avg:.1f} kW</b> matching regional solar irradiance curves. Sizing a 50–100 kWp grid-tied solar array over the Academic Building and Lecture Hall can offset grid import by 30–45% during peak hours.",
         "Renewable Generation"),
        ("💡", "High-Efficiency LED & Daylight Harvesting Retrofit",
         "Convert any residual fluorescent/HID fixtures across Central Library and Academic Hall to 140 lm/W smart LED troffers equipped with integrated photocells.",
         "Standard Efficiency Upgrade")
    ]

    for icon, title, desc, tag in recs:
        st.markdown(f"""
            <div class="rec-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                    <span style="font-weight:700; color:#FFFFFF; font-size:1.05rem;">{icon} {title}</span>
                    <span style="background:rgba(0,240,255,0.1); color:#00F0FF; border:1px solid rgba(0,240,255,0.3); font-size:0.7rem; font-weight:700; padding:2px 8px; border-radius:9999px;">{tag}</span>
                </div>
                <div style="color:#94A3B8; font-size:0.9rem; line-height:1.5;">{desc}</div>
            </div>
        """, unsafe_allow_html=True)

# ======================== DATA QUALITY ========================
elif page == "Data Quality":
    st.markdown("""
        <div class="page-header-box">
            <h1 class="page-header-title">Data Integrity & Metrology Audit</h1>
            <p class="page-header-desc">Sensor telemetry coverage analysis, missing reading percentages per building, and historical uptime metrics.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("📡", "Telemetry Records", f"{len(df):,}", "1-minute resolution readings")
    with c2:
        render_kpi("📅", "Monitoring Horizon", f"{df['timestamp'].dt.year.nunique()} Years", f"{df['timestamp'].min().strftime('%b %Y')} – {df['timestamp'].max().strftime('%b %Y')}")
    with c3:
        render_kpi("🏢", "Meters Polled", "9 Channels", "100% active metering coverage")
    with c4:
        render_kpi("⚡", "Sample Frequency", "60 Seconds", "Nominal data polling cadence")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    col_tbl_q, col_bar_q = st.columns([1, 1.2])

    missing_pct = (df[BUILDINGS].isnull().sum() / len(df) * 100).sort_values(ascending=False)

    with col_tbl_q:
        st.markdown("<div class='section-title'><span>Telemetry Quality Matrix</span></div>", unsafe_allow_html=True)
        missing_df = pd.DataFrame({
            "Facility": [friendly(c) for c in missing_pct.index],
            "Missing (%)": missing_pct.values.round(2),
            "Uptime (%)": (100 - missing_pct.values).round(2),
            "Lost Samples": df[BUILDINGS].isnull().sum().reindex(missing_pct.index).values
        })
        st.dataframe(missing_df, width="stretch", height=360, hide_index=True)

    with col_bar_q:
        st.markdown("<div class='section-title'><span>Missing Telemetry by Meter (%)</span></div>", unsafe_allow_html=True)
        fig_miss = px.bar(
            x=[friendly(c) for c in missing_pct.index],
            y=missing_pct.values,
            labels={"x": "Meter Location", "y": "Missing Rate (%)"},
            color=missing_pct.values,
            color_continuous_scale=[[0, "#0D9488"], [0.5, "#F59E0B"], [1, "#F43F5E"]],
            text=[f"{v:.1f}%" for v in missing_pct.values]
        )
        fig_miss.update_traces(
            textposition='outside',
            textfont=dict(color='#CBD5E1', size=10),
            hovertemplate="<b>%{x}:</b> %{y:.2f}% missing<extra></extra>"
        )
        fig_miss.update_coloraxes(showscale=False)
        apply_chart_theme(fig_miss, height=360)
        fig_miss.update_xaxes(tickangle=-30)
        st.plotly_chart(fig_miss, width="stretch")

    st.markdown("<div class='section-title'><span>Mean Active Meters Polled Daily (Max 9)</span></div>", unsafe_allow_html=True)
    df["valid_count"] = df[BUILDINGS].notna().sum(axis=1)
    daily_coverage = df.groupby("date")["valid_count"].mean()
    daily_coverage.index = pd.to_datetime(daily_coverage.index)

    fig_cov = px.line(
        x=daily_coverage.index,
        y=daily_coverage.values,
        labels={"x": "Date", "y": "Operational Meters"},
        color_discrete_sequence=["#00F0FF"]
    )
    fig_cov.add_hline(
        y=9,
        line_dash="dash",
        line_color="#10B981",
        annotation_text="Ideal Uptime (All 9 Meters Active)",
        annotation_position="bottom right"
    )
    apply_chart_theme(fig_cov, height=320)
    fig_cov.update_layout(yaxis_range=[0, 9.5])
    st.plotly_chart(fig_cov, width="stretch")

    st.markdown("<div class='section-title'><span>Monthly Missing Telemetry Matrix</span></div>", unsafe_allow_html=True)
    df["year_month"] = df["timestamp"].dt.to_period("M").astype(str)
    monthly_missing = (df.groupby("year_month")[BUILDINGS].apply(lambda g: g.isnull().mean() * 100).round(1))
    monthly_missing.columns = [friendly(c) for c in monthly_missing.columns]

    fig_hm2 = px.imshow(
        monthly_missing.T,
        labels={"x": "Month", "y": "Facility", "color": "Missing (%)"},
        color_continuous_scale=[[0, "#081226"], [0.25, "#1E3A8A"], [0.6, "#D97706"], [1, "#DC2626"]],
        aspect="auto"
    )
    apply_chart_theme(fig_hm2, height=380)
    fig_hm2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_hm2, width="stretch")


