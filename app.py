"""
Eden Sovereign Intelligence Terminal v2026
Institutional-grade equity research terminal.
"""

import warnings
warnings.filterwarnings("ignore")

import json
import os
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Eden Sovereign | v2026",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="expanded")

# ── Ticker universe ───────────────────────────────────────────────────────────
TICKER_LIST = sorted(set([
    # Mag 7
    'AAPL','MSFT','NVDA','AMZN','GOOG','GOOGL','META','TSLA',
    # Semiconductors
    'AVGO','AMD','INTC','QCOM','TXN','AMAT','MU','LRCX','KLAC','MRVL',
    'ARM','NXPI','ON','SWKS','QRVO','MPWR','SMCI','ONTO','ACLS','WOLF',
    'AMBA','SLAB','DIOD','POWI','SITM','CRUS','MTSI','LSCC','ALGM',
    'TSM','ASML','UMC','HIMX','AEHR',
    # Software / Cloud / SaaS
    'ORCL','CRM','ADBE','NOW','INTU','WDAY','VEEV','TEAM','ZM','OKTA',
    'TWLO','TTD','HUBS','ZS','DDOG','SNOW','MDB','GTLB','ESTC','APPN','PCTY','PAYC','GWRE','JAMF','TENB',
    'QLYS','CHKP','FTNT','PANW','CRWD','S','CYBR','RPM','VRNS',
    'NCNO','DOCU','BOX','DOCN','FSLY','BILL',
    # Big Tech / Hardware
    'IBM','CSCO','HPQ','HPE','DELL','WDC','STX','NTAP','JNPR','ZBRA',
    'VRSN','FFIV','CTSH','EPAM','GDDY','AKAM','CDW','NSIT','ACN',
    'LDOS','SAIC','BAH','CACI',
    # Internet / Consumer Tech
    'NFLX','UBER','LYFT','ABNB','DASH','RBLX','SNAP','PINS','SHOP',
    'MELI','SE','BIDU','JD','PDD','BABA','TCOM','NTES','BILI','IQ',
    'ZTO','EDU','TAL','WB','DOYU','HUYA','VIPS',
    'ETSY','EBAY','CHWY','W','RVLV','REAL','ROKU','SPOT','SIRI',
    # Crypto / Blockchain
    'COIN','MSTR','HOOD','RIOT','MARA','HUT','CLSK','BTBT','CIFR',
    'BITF','IREN','WULF','HIVE',
    # AI / Emerging Tech
    'PLTR','SOUN','AI','BBAI','IONQ','QUBT','RGTI','ARQQ','ONDS',
    'KULR','BFLY','RCAT','OUST','INVZ',
    # Fintech
    'SQ','PYPL','SOFI','AFRM','UPST','LC','NU','ALLY','DFS','SYF',
    'CACC','NAVI','GPN','FIS','FISV','WEX','RPAY','FLYW','CURO',
    # Banks / Financials
    'JPM','BAC','GS','MS','WFC','C','USB','TFC','PNC','COF',
    'AXP','V','MA','BLK','SCHW','STT','BK','NTRS','AMP','BEN',
    'TROW','IVZ','RJF','SF','LPLA',
    'MCO','SPGI','MSCI','ICE','CME','NDAQ','CBOE',
    'BX','KKR','APO','ARES','CG','BN','BAM','OWL','HLNE','TPG',
    # Insurance
    'PGR','ALL','TRV','AIG','HIG','CB','MKL','RNR','RE','WRB',
    'CINF','AFL','MET','PRU','LNC','UNM','GL','FG','RLI',
    # Healthcare / Pharma
    'UNH','LLY','JNJ','ABBV','MRK','PFE','AMGN','GILD','REGN',
    'ISRG','TMO','DHR','ZTS','SYK','MDT','ABT','ELV','CI','HUM','CVS',
    'MCK','CAH','COR','HSIC',
    'BMY','AZN','GSK','NVS','SNY','BAYRY',
    'MRNA','BNTX','NVAX','VRTX','BIIB','ILMN','ALGN','HOLX',
    'RMD','DXCM','IDXX','MTD','WAT','A','BRKR','TECH',
    'HCA','THC','UHS','DVA','ENSG','NHC',
    'IQV','CTLT','PRGO','JAZZ','EXAS','NTRA','GH','ACAD','SAGE',
    'INCY','ALNY','BMRN','SRPT','RARE','FOLD','KYMR',
    # Consumer Discretionary
    'WMT','COST','TGT','HD','LOW','MCD','SBUX','NKE','LULU','ULTA',
    'RL','TPR','CPRI','VFC','HBI','PVH','UAA','UA','ONON','SKX','CROX',
    'CMG','DPZ','QSR','YUM','DNUT','JACK','SHAK','WING','TXRH','EAT',
    'DRI','CAKE','F','GM','STLA','RIVN','NIO','LCID','XPEV','LI','BKNG','EXPE','TRIP','MAR','HLT','H','IHG','CHH',
    'MGM','WYNN','LVS','CZR','PENN','DKNG','BYD','CHDN',
    'CCL','RCL','NCLH',
    'PTON','DKS','ASO',# Consumer Staples
    'PG','KO','PEP','PM','MO','MDLZ','CL','KHC','GIS','K','CPB',
    'CAG','HRL','SJM','MKC','CHD','CLX','EL','COTY','IPAR',
    'STZ','BUD','TAP','SAM','MNST','KDP','FIZZ','CELH',
    'SYY','USFD','PFGC','CHEF',
    # Energy
    'XOM','CVX','COP','EOG','SLB','OXY','PSX','VLO','MPC','DVN',
    'HAL','BKR','NOV','HP','PTEN','RIG','VAL','DO','NE','FTI',
    'PXD','FANG','APA','MRO','HES','CNX','EQT','RRC','AR','SWN',
    'KMI','WMB','OKE','ET','EPD','TRGP','PAA','MPLX','LNG',
    # Utilities / Clean Energy
    'NEE','AES','D','DUK','SO','EXC','PCG','ED','FE','AEE','CMS',
    'WEC','XEL','ES','PEG','ETR','EVRG','NI','OGE',
    'FSLR','ENPH','SEDG','NOVA','RUN','SPWR','SHLS','STEM','ARRY','BE',
    # Industrials / Defense
    'BA','LMT','RTX','GE','HON','CAT','DE','UPS','NSC','GD','NOC',
    'TDG','LHX','KTOS','AXON','CACI','HII','AVAV','JOBY',
    'MMM','EMR','ITW','ROK','PH','AME','DOV','IR','XYL',
    'FLR','J','KBR','PWR','MTZ','DY','NVEE','PRIM','MYR',
    'FDX','XPO','SAIA','JBHT','WERN','CHRW','EXPD','GXO',
    'DAL','AAL','UAL','LUV','ALK','SKYW',
    'GPC','LKQ','APTV','LEA','BWA','GNTX','TEN','GT',
    'FAST','GWW','MSM','AIT','TTC','AGCO','CNH','LNN',
    'OTIS','CARR','TT','JCI',
    # Materials
    'LIN','APD','ALB','PPG','SHW','RPM','FMC','ECL','IFF','AVNT',
    'CE','HUN','WLK','LYB','OLN','CC','EMN','PKG','IP','WRK','SEE',
    'NUE','STLD','X','CLF','RS','CMC','MP','ARNC','AA','CENX',
    'FCX','NEM','AEM','GOLD','KGC','AU','GFI','WPM','PAAS','SILV',
    'RIO','BHP','VALE','SCCO','TECK','FM','HBM','SQM','LTHM',
    # Real Estate
    'AMT','PLD','EQIX','CCI','SBAC','DLR','PSA','EXR','CUBE',
    'SPG','O','NNN','ADC','EPRT','KIM','REG','BRX',
    'ARE','BXP','SLG','VNO','HPP','WELL','VTR','OHI','NHI','CTRE','LTC','SBRA',
    'EQR','AVB','UDR','CPT','ESS','IRT',
    # Communication Services
    'T','VZ','TMUS','LUMN','TDS','USM','IDT','OOMA',
    'DIS','CMCSA','WBD','PARA','AMC','NWSA','NWS','FOXA','FOX',
    'NYT','IAC',
    # Space / Aerospace
    'SPCE','RKLB','ASTS','PL','BWXT',
    'ACHR','JOBY','BLDE','EHANG',
    # Gaming / Leisure
    'EA','TTWO','RBLX',
    # Meme / Retail Favorites
    'GME','AMC','BB','NOK','SNDL','TLRY','CGC','ACB','CRON',
    'CLOV','WKHS','NKLA',
    # International ADRs
    'SAP','SONY','TM','HMC','NVS','AZN','GSK','BP','SHEL','TTE',
    'BABA','JD','PDD','BIDU','NIO','XPEV','LI','NTES',
    'SE','GRAB','MELI','NU','ITUB',
    'RIO','BHP','VALE','TECK','SQM',
    'IRE','ING','CS','UBS','DB','HSBC','BCS','LYG','MFG','SMFG',
    # ETFs (popular)
    'SPY','QQQ','IWM','DIA','VTI','VOO','IVV',
    'XLK','XLF','XLE','XLV','XLI','XLU','XLB','XLRE','XLC','XLY','XLP',
    'GLD','SLV','GDX','GDXJ','USO','UNG','TLT','AGG','HYG','LQD',
    'ARKK','ARKG','ARKW','ARKF','ARKX',
    'SOXL','TQQQ','UPRO','SPXL','TECL','FNGU',
    # Misc / Other
    'BRK-B','BRK-A','MMM','TRMB','GDDY',
    'BALL','SON','AMCR','BERY','OC','SOLV']))

SECTOR_GROUPS: dict[str, list[str]] = {
    "Mag 7": ["AAPL","MSFT","NVDA","AMZN","GOOG","GOOGL","META","TSLA"],
    "Semiconductors": [
        "NVDA","AMD","INTC","QCOM","AVGO","TXN","AMAT","MU","LRCX","KLAC",
        "MRVL","ARM","NXPI","ON","SWKS","QRVO","MPWR","SMCI","ONTO","ACLS",
        "WOLF","AMBA","SLAB","DIOD","POWI","SITM","CRUS","MTSI","LSCC","ALGM",
        "TSM","ASML","UMC","HIMX","AEHR"],
    "Software / Cloud / SaaS": [
        "MSFT","ORCL","CRM","ADBE","NOW","INTU","WDAY","VEEV","TEAM","ZM",
        "OKTA","TWLO","TTD","HUBS","ZS","DDOG","SNOW","MDB","GTLB","ESTC",
        "APPN","PCTY","PAYC","GWRE","JAMF","TENB",
        "QLYS","CHKP","FTNT","PANW","CRWD","S","CYBR","VRNS","NCNO",
        "DOCU","BOX","DOCN","FSLY","BILL"],
    "Big Tech / Hardware": [
        "AAPL","GOOG","GOOGL","META","IBM","CSCO","HPQ","HPE","DELL","WDC",
        "STX","NTAP","JNPR","ZBRA","VRSN","FFIV","CTSH","EPAM","GDDY","AKAM",
        "CDW","NSIT","ACN","LDOS","SAIC","BAH","CACI"],
    "Internet / Consumer Tech": [
        "AMZN","NFLX","UBER","LYFT","ABNB","DASH","RBLX","SNAP","PINS","SHOP",
        "MELI","SE","BIDU","JD","PDD","BABA","TCOM","NTES","BILI","IQ",
        "ZTO","EDU","TAL","WB","DOYU","HUYA","VIPS",
        "ETSY","EBAY","CHWY","W","RVLV","REAL","ROKU","SPOT","SIRI"],
    "Crypto / Blockchain": [
        "COIN","MSTR","HOOD","RIOT","MARA","HUT","CLSK","BTBT","CIFR",
        "BITF","IREN","WULF","HIVE"],
    "AI / Emerging Tech": [
        "NVDA","PLTR","SOUN","AI","BBAI","IONQ","QUBT","RGTI","ARQQ","ONDS",
        "KULR","BFLY","RCAT","OUST","INVZ"],
    "Fintech": [
        "SQ","PYPL","SOFI","AFRM","UPST","LC","NU","ALLY","DFS","SYF",
        "CACC","NAVI","GPN","FIS","FISV","WEX","RPAY","FLYW","CURO"],
    "Banks": [
        "JPM","BAC","GS","MS","WFC","C","USB","TFC","PNC","COF",
        "AXP","V","MA"],
    "Asset Management / Exchanges": [
        "BLK","SCHW","STT","BK","NTRS","AMP","BEN","TROW","IVZ","RJF","SF","LPLA",
        "MCO","SPGI","MSCI","ICE","CME","NDAQ","CBOE",
        "BX","KKR","APO","ARES","CG","BN","BAM","OWL","HLNE","TPG"],
    "Insurance": [
        "PGR","ALL","TRV","AIG","HIG","CB","MKL","RNR","RE","WRB",
        "CINF","AFL","MET","PRU","LNC","UNM","GL","FG","RLI"],
    "Healthcare / Managed Care": [
        "UNH","ELV","CI","HUM","CVS","MCK","CAH","COR","HSIC",
        "HCA","THC","UHS","DVA","ENSG","NHC"],
    "Pharma / Biotech Large": [
        "LLY","JNJ","ABBV","MRK","PFE","AMGN","GILD","REGN","BMY",
        "AZN","GSK","NVS","SNY","BAYRY"],
    "Biotech / Genomics": [
        "MRNA","BNTX","NVAX","VRTX","BIIB","ILMN","ALGN","HOLX",
        "INCY","ALNY","BMRN","SRPT","RARE","FOLD","KYMR",
        "ACAD","SAGE"],
    "MedTech / Devices": [
        "ISRG","TMO","DHR","ZTS","SYK","MDT","ABT","RMD","DXCM",
        "IDXX","MTD","WAT","A","BRKR","TECH",
        "IQV","CTLT","PRGO","JAZZ","EXAS","NTRA","GH"],
    "Consumer Discretionary": [
        "AMZN","WMT","COST","TGT","HD","LOW","MCD","SBUX","NKE","LULU","ULTA",
        "RL","TPR","CPRI","VFC","HBI","PVH","UAA","UA","ONON","SKX","CROX",
        "CMG","DPZ","QSR","YUM","DNUT","JACK","SHAK","WING","TXRH","EAT",
        "DRI","CAKE","BKNG","EXPE","TRIP","MAR","HLT","H","IHG","CHH",
        "PTON","DKS","ASO","ETSY","EBAY","CHWY","W","RVLV","REAL"],
    "Autos / EVs": [
        "TSLA","F","GM","STLA","RIVN","NIO","LCID","XPEV","LI"],
    "Casinos / Gaming Leisure": [
        "MGM","WYNN","LVS","CZR","PENN","DKNG","BYD","CHDN",
        "CCL","RCL","NCLH"],
    "Consumer Staples": [
        "WMT","COST","PG","KO","PEP","PM","MO","MDLZ","CL","KHC","GIS",
        "K","CPB","CAG","HRL","SJM","MKC","CHD","CLX","EL","COTY","IPAR",
        "STZ","BUD","TAP","SAM","MNST","KDP","FIZZ","CELH",
        "SYY","USFD","PFGC","CHEF"],
    "Energy - Majors": [
        "XOM","CVX","COP","OXY","PSX","VLO","MPC","DVN",
        "PXD","FANG","APA","MRO","HES","CNX","EQT","RRC","AR","SWN"],
    "Energy - Services / Drilling": [
        "SLB","EOG","HAL","BKR","NOV","HP","PTEN","RIG","VAL","DO","FTI"],
    "Midstream / Pipelines": [
        "KMI","WMB","OKE","ET","EPD","TRGP","PAA","MPLX","LNG"],
    "Utilities": [
        "NEE","AES","D","DUK","SO","EXC","PCG","ED","FE","AEE","CMS",
        "WEC","XEL","ES","PEG","ETR","EVRG","NI","OGE"],
    "Clean Energy / Solar": [
        "NEE","FSLR","ENPH","SEDG","NOVA","RUN","SPWR","SHLS","STEM","ARRY","BE"],
    "Defense / Aerospace": [
        "BA","LMT","RTX","GE","GD","NOC","TDG","LHX","KTOS","AXON",
        "HII","AVAV","JOBY","BWXT"],
    "Industrials - Diversified": [
        "HON","CAT","DE","UPS","NSC","MMM","EMR","ITW","ROK","PH",
        "AME","DOV","IR","XYL","OTIS","CARR","TT","JCI"],
    "Engineering / Construction": [
        "FLR","J","KBR","PWR","MTZ","DY","NVEE","PRIM","MYR"],
    "Logistics / Transport": [
        "UPS","FDX","XPO","SAIA","JBHT","WERN","CHRW","EXPD","GXO"],
    "Airlines": [
        "DAL","AAL","UAL","LUV","ALK","SKYW"],
    "Auto Parts": [
        "GPC","LKQ","APTV","LEA","BWA","GNTX","TEN","GT"],
    "Industrial Distribution": [
        "FAST","GWW","MSM","AIT","TTC","AGCO","CNH","LNN"],
    "Chemicals": [
        "LIN","APD","PPG","SHW","RPM","FMC","ECL","IFF","AVNT",
        "CE","HUN","WLK","LYB","OLN","CC","EMN"],
    "Packaging": [
        "PKG","IP","WRK","SEE","AMCR","BERY","OC","BALL","SON"],
    "Metals - Steel": [
        "NUE","STLD","X","CLF","RS","CMC","ARNC","AA","CENX"],
    "Metals - Mining": [
        "ALB","MP","FCX","NEM","AEM","GOLD","KGC","AU","GFI","WPM","PAAS","SILV",
        "RIO","BHP","VALE","SCCO","TECK","FM","HBM","SQM","LTHM"],
    "REITs - Data / Industrial": [
        "AMT","PLD","EQIX","CCI","SBAC","DLR","PSA","EXR","CUBE"],
    "REITs - Retail": [
        "SPG","O","NNN","ADC","EPRT","KIM","REG","BRX"],
    "REITs - Office": [
        "ARE","BXP","SLG","VNO","HPP"],
    "REITs - Healthcare": [
        "WELL","VTR","OHI","NHI","CTRE","LTC","SBRA"],
    "REITs - Residential": [
        "EQR","AVB","UDR","CPT","ESS","IRT"],
    "Telecom": [
        "T","VZ","TMUS","LUMN","TDS","USM","IDT","OOMA"],
    "Media / Entertainment": [
        "DIS","NFLX","CMCSA","WBD","PARA","AMC","NWSA","NWS","FOXA","FOX",
        "NYT","IAC","EA","TTWO","RBLX"],
    "Space / Aerospace Emerging": [
        "SPCE","RKLB","ASTS","PL","ACHR","JOBY","BLDE","EHANG"],
    "Meme / Retail": [
        "GME","AMC","BB","NOK","SNDL","TLRY","CGC","ACB","CRON",
        "CLOV","WKHS","NKLA"],
    "International ADRs - Europe": [
        "SAP","NVS","AZN","GSK","BP","SHEL","TTE","IRE","ING","CS","UBS",
        "DB","HSBC","BCS","LYG","MFG","SMFG"],
    "International ADRs - Asia": [
        "TSM","ASML","SONY","TM","HMC","BABA","JD","PDD","BIDU","NIO",
        "XPEV","LI","NTES","SE","GRAB","MELI","NU","ITUB","RIO","BHP",
        "VALE","TECK","SQM"],
    "ETFs - Broad Market": [
        "SPY","QQQ","IWM","DIA","VTI","VOO","IVV"],
    "ETFs - Sector": [
        "XLK","XLF","XLE","XLV","XLI","XLU","XLB","XLRE","XLC","XLY","XLP"],
    "ETFs - Commodities / Bonds": [
        "GLD","SLV","GDX","GDXJ","USO","UNG","TLT","AGG","HYG","LQD"],
    "ETFs - Thematic": [
        "ARKK","ARKG","ARKW","ARKF","ARKX",
        "SOXL","TQQQ","UPRO","SPXL","TECL","FNGU"],
}

# legacy compat alias (used by get_peers_for)
PEERS: dict[str, list[str]] = {}


MEGA_CAP_THRESHOLD = 200e9

# ── Global Defense Layer ─────────────────────────────────────────────────────
sector_val="N/A"; mkt_cap=0.0; pe_ratio=float("nan"); peg_ratio=float("nan")
gross_margins=float("nan"); revenue_cagr=0.0; fcf_yield=0.0
current_price=0.0; prev_close=0.0; ma50=float("nan"); ma200=float("nan")
rsi_val=50.0; macd_hist_val=0.0; company_name="N/A"
forward_pe=float("nan"); dividend_yield=0.0
analyst_target_mean=float("nan"); analyst_target_high=float("nan")
analyst_target_low=float("nan"); n_analysts=0; rec_key="N/A"

# ── Indicator config ──────────────────────────────────────────────────────────
OVERLAY_INDS  = {"Bollinger Bands", "VWAP"}
SUBPLOT_INDS  = ["RSI", "MACD", "Stochastic", "OBV", "ATR"]
ALL_INDS      = ["Bollinger Bands", "VWAP", "RSI", "MACD", "Stochastic", "OBV", "ATR"]

# ── Best Pick Universe ────────────────────────────────────────────────────────
BEST_PICK_UNIVERSE = [
    "AAPL","MSFT","NVDA","AMZN","META","TSLA","GOOG","AVGO",
    "LLY","JPM","V","MA","UNH","XOM","PLTR","AMD","CRM","COST",
    "NFLX","ORCL","NOW","ISRG","GS","BX","COIN","SQ","MELI","SE",
]

# ── Eden Color Palette ────────────────────────────────────────────────────────
EDEN_COLORS = ["#6366f1","#10b981","#f59e0b","#ef4444","#8b5cf6",
               "#06b6d4","#f97316","#84cc16","#ec4899","#14b8a6"]


# ── CSS ───────────────────────────────────────────────────────────────────────
def inject_css(account_label: str = "&#128100; Sandbox Mode", is_logged_in: bool = False) -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    #MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"]{visibility:hidden;display:none}

    html,body,[class*="css"]{font-family:'Inter',-apple-system,sans-serif;background-color:#fcfcfc}

    [data-testid="stSidebar"]{
        background:linear-gradient(180deg,#f8f9ff 0%,#f0f1ff 100%);
        border-right:1px solid rgba(99,102,241,.12);
    }

    .eden-logo{display:flex;align-items:center;gap:12px;padding:8px 4px 20px;
               border-bottom:1px solid rgba(99,102,241,.15);margin-bottom:20px}
    .eden-icon{width:44px;height:44px;background:linear-gradient(135deg,#6366f1,#8b5cf6);
               border-radius:12px;display:flex;align-items:center;justify-content:center;
               color:#fff;font-weight:700;font-size:22px;box-shadow:0 4px 12px rgba(99,102,241,.35);flex-shrink:0}
    .eden-brand{font-size:14px;font-weight:700;color:#1a1a2e;letter-spacing:-.3px}
    .eden-sub{font-size:10px;color:#6366f1;letter-spacing:1.5px;text-transform:uppercase}

    .metric-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:20px 0 16px}
    .metric-card{background:rgba(255,255,255,.75);backdrop-filter:blur(10px);
                 border:1px solid rgba(99,102,241,.18);border-radius:16px;padding:18px 16px;
                 box-shadow:0 4px 24px rgba(99,102,241,.07);transition:transform .2s,box-shadow .2s}
    .metric-card:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(99,102,241,.13)}
    .metric-label{font-size:10px;font-weight:600;color:#6366f1;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:6px}
    .metric-value{font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:600;color:#1a1a2e;line-height:1.2}
    .metric-sub{font-size:11px;font-weight:500;margin-top:4px}
    .positive{color:#10b981} .negative{color:#ef4444} .neutral{color:#6b7280}

    .analyst-card{background:rgba(255,255,255,.75);backdrop-filter:blur(10px);
                  border:1px solid rgba(99,102,241,.18);border-radius:16px;padding:20px 24px;
                  margin:0 0 20px;box-shadow:0 4px 24px rgba(99,102,241,.07);
                  display:flex;gap:40px;align-items:center;flex-wrap:wrap}
    .analyst-block{display:flex;flex-direction:column;gap:4px}
    .analyst-lbl{font-size:10px;font-weight:600;color:#6366f1;letter-spacing:1.2px;text-transform:uppercase}
    .analyst-val{font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:600;color:#1a1a2e}
    .analyst-sub{font-size:11px;color:#6b7280}
    .price-bar-track{height:6px;background:#e5e7eb;border-radius:3px;margin:8px 0}
    .price-bar-fill{height:6px;background:linear-gradient(90deg,#10b981,#6366f1);border-radius:3px}
    .price-bar-labels{display:flex;justify-content:space-between;font-size:10px;color:#9ca3af;font-family:'JetBrains Mono',monospace}
    .rec-badge{display:inline-flex;align-items:center;padding:4px 14px;border-radius:20px;font-weight:700;font-size:13px;font-family:'JetBrains Mono',monospace}

    .score-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 18px;border-radius:50px;
                 font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:700;margin-left:16px}

    .ticker-header{display:flex;align-items:baseline;gap:12px;margin-bottom:4px}
    .ticker-symbol{font-size:32px;font-weight:700;color:#1a1a2e;letter-spacing:-1px}
    .company-full{font-size:14px;color:#6b7280;font-weight:400}

    .exec-card{background:#fff;border-radius:20px;padding:36px 40px;
               border:1px solid rgba(99,102,241,.12);box-shadow:0 2px 20px rgba(0,0,0,.04);margin-top:8px}

    .ceo-summary{border-left:4px solid #6366f1;padding:16px 20px;
                 background:linear-gradient(90deg,rgba(99,102,241,.04),transparent);
                 border-radius:0 12px 12px 0;margin-bottom:32px}
    .ceo-summary-title{font-size:11px;font-weight:700;color:#6366f1;
                       letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px}
    .ceo-summary p{font-size:1.02rem;line-height:1.85;color:#1a1a2e;margin:0 0 10px}
    .ceo-summary p:last-child{margin:0}

    .report-section{margin-bottom:28px}
    .report-section-title{font-size:13px;font-weight:700;color:#1a1a2e;margin-bottom:14px;
                          padding-bottom:8px;border-bottom:1px solid rgba(99,102,241,.1)}
    .rpt-row{display:flex;align-items:center;justify-content:space-between;
             padding:9px 0;border-bottom:1px solid #f3f4f6}
    .rpt-row:last-child{border-bottom:none}
    .rpt-name{font-size:13px;color:#374151;font-weight:500}
    .rpt-value{font-family:'JetBrains Mono',monospace;font-size:13px;color:#1a1a2e;font-weight:600}
    .badge{font-size:10px;font-weight:700;padding:2px 10px;border-radius:20px;letter-spacing:.5px;text-transform:uppercase}
    .badge-green{background:rgba(16,185,129,.12);color:#059669}
    .badge-yellow{background:rgba(245,158,11,.12);color:#d97706}
    .badge-red{background:rgba(239,68,68,.12);color:#dc2626}
    .badge-blue{background:rgba(99,102,241,.12);color:#6366f1}
    .badge-gray{background:#f3f4f6;color:#6b7280}

    .thesis-list{list-style:none;padding:0;margin:0}
    .thesis-item{display:flex;gap:10px;padding:10px 0;border-bottom:1px solid #f3f4f6;
                 font-size:13px;color:#374151;line-height:1.6}
    .thesis-item:last-child{border-bottom:none}
    .thesis-icon{flex-shrink:0;font-size:14px;margin-top:1px}
    .thesis-title{font-weight:600;color:#1a1a2e}

    .verdict-box{background:linear-gradient(135deg,#f0f1ff,#faf0ff);border-radius:14px;
                 padding:22px 28px;border:1px solid rgba(99,102,241,.2);margin-top:28px;
                 display:flex;align-items:center;gap:20px;flex-wrap:wrap}
    .verdict-label{font-size:1.5rem;font-weight:800}
    .verdict-meta{font-family:'JetBrains Mono',monospace;font-size:12px;color:#6b7280;line-height:1.8}

    .hero{text-align:center;padding:80px 20px;color:#9ca3af}
    .hero h1{font-size:2rem;font-weight:700;color:#1a1a2e;margin-bottom:8px}

    [data-testid="stTabs"] [role="tab"]{font-family:'Inter',sans-serif;font-size:13px;font-weight:600;color:#6b7280}
    [data-testid="stTabs"] [role="tab"][aria-selected="true"]{color:#6366f1}

    .news-card{padding:14px 0;border-bottom:1px solid #f3f4f6}
    .news-card:last-child{border-bottom:none}
    .news-title a{font-size:14px;font-weight:600;color:#1a1a2e;text-decoration:none;line-height:1.5}
    .news-title a:hover{color:#6366f1}
    .news-meta{font-size:11px;color:#9ca3af;margin-top:4px}
    .earn-next{background:linear-gradient(90deg,rgba(99,102,241,.06),transparent);
               border-left:4px solid #6366f1;border-radius:0 10px 10px 0;
               padding:12px 18px;margin-bottom:20px;font-size:14px;color:#1a1a2e;font-weight:500}

    /* Clickable financial terms in Report */
    .term{border-bottom:1.5px dashed rgba(99,102,241,.55);color:#6366f1;cursor:help;
          position:relative;display:inline-block;font-weight:600;white-space:nowrap}
    .term::after{content:attr(data-def);position:absolute;bottom:130%;left:50%;
                 transform:translateX(-50%);background:#1a1a2e;color:#f3f4f6;
                 padding:10px 14px;border-radius:10px;font-size:12px;font-weight:400;
                 width:270px;z-index:9999;line-height:1.65;
                 box-shadow:0 8px 24px rgba(0,0,0,.3);white-space:normal;
                 pointer-events:none;opacity:0;transition:opacity .15s}
    .term:hover::after{opacity:1}

    /* Peers add-stock row */
    .peers-add{display:flex;gap:10px;align-items:center;margin-top:16px;
               padding:14px 18px;background:rgba(99,102,241,.04);
               border:1px dashed rgba(99,102,241,.25);border-radius:12px}

    /* ── 3-Dots Settings Menu ─────────────────────────────────────────── */
    #eden-dots-btn{position:fixed;top:14px;right:14px;z-index:99999;
        width:38px;height:38px;border-radius:50%;
        background:rgba(255,255,255,.92);backdrop-filter:blur(8px);
        border:1.5px solid rgba(99,102,241,.3);cursor:pointer;
        font-size:22px;font-weight:900;display:flex;align-items:center;
        justify-content:center;box-shadow:0 3px 14px rgba(0,0,0,.12);
        color:#6366f1;user-select:none;line-height:1;transition:box-shadow .18s}
    #eden-dots-btn:hover{box-shadow:0 5px 18px rgba(99,102,241,.28)}
    #eden-menu-backdrop{display:none;position:fixed;inset:0;z-index:99996}
    html:has(#eden-menu-chk:checked) #eden-menu-backdrop{display:block}
    #eden-panel{position:fixed;top:58px;right:14px;z-index:99998;
        background:#fff;border-radius:16px;padding:8px 0;
        border:1px solid rgba(99,102,241,.18);
        box-shadow:0 8px 32px rgba(0,0,0,.13);min-width:210px;
        opacity:0;transform:scale(.95) translateY(-6px);
        pointer-events:none;transition:opacity .18s,transform .18s}
    html:has(#eden-menu-chk:checked) #eden-panel{
        opacity:1;transform:scale(1) translateY(0);pointer-events:auto}
    .eden-panel-title{font-size:10px;font-weight:700;color:#9ca3af;
        letter-spacing:1.2px;text-transform:uppercase;padding:6px 16px 10px}
    .eden-panel-item{display:flex;align-items:center;justify-content:space-between;
        padding:10px 16px;cursor:pointer;font-size:13px;color:#1a1a2e;
        font-weight:500;transition:background .12s;gap:10px}
    .eden-panel-item:hover{background:rgba(99,102,241,.06)}
    .eden-panel-sep{height:1px;background:rgba(99,102,241,.1);margin:4px 0}
    .eden-toggle{width:34px;height:20px;background:#d1d5db;border-radius:10px;
        position:relative;transition:background .2s;flex-shrink:0}
    .eden-toggle-knob{position:absolute;top:3px;left:3px;width:14px;height:14px;
        background:#fff;border-radius:50%;transition:transform .2s;
        box-shadow:0 1px 4px rgba(0,0,0,.2)}
    html:has(#eden-dark-chk:checked) .eden-toggle{background:#6366f1}
    html:has(#eden-dark-chk:checked) .eden-toggle-knob{transform:translateX(14px)}

    /* ── Dark Mode (pure CSS via :has) ────────────────────────────────── */
    html:has(#eden-dark-chk:checked) body,
    html:has(#eden-dark-chk:checked) .stApp,
    html:has(#eden-dark-chk:checked) .block-container,
    html:has(#eden-dark-chk:checked) .stMainBlockContainer,
    html:has(#eden-dark-chk:checked) [class*="css"]{background-color:#0f0f1a!important;color:#e2e2f0!important}
    html:has(#eden-dark-chk:checked) [data-testid="stSidebar"]{background:linear-gradient(180deg,#1a1a2e 0%,#16162a 100%)!important;border-right-color:rgba(99,102,241,.25)!important}
    html:has(#eden-dark-chk:checked) .metric-card,
    html:has(#eden-dark-chk:checked) .analyst-card{background:rgba(26,26,46,.85)!important;border-color:rgba(99,102,241,.3)!important}
    html:has(#eden-dark-chk:checked) .metric-value,
    html:has(#eden-dark-chk:checked) .ticker-symbol,
    html:has(#eden-dark-chk:checked) .eden-brand,
    html:has(#eden-dark-chk:checked) .analyst-val,
    html:has(#eden-dark-chk:checked) .report-section-title,
    html:has(#eden-dark-chk:checked) .rpt-value,
    html:has(#eden-dark-chk:checked) .rpt-name,
    html:has(#eden-dark-chk:checked) .hero h1,
    html:has(#eden-dark-chk:checked) .earn-next,
    html:has(#eden-dark-chk:checked) .ceo-summary p,
    html:has(#eden-dark-chk:checked) .thesis-item{color:#e2e2f0!important}
    html:has(#eden-dark-chk:checked) .metric-label,
    html:has(#eden-dark-chk:checked) .analyst-lbl{color:#a78bfa!important}
    html:has(#eden-dark-chk:checked) .exec-card{background:#1a1a2e!important;border-color:rgba(99,102,241,.25)!important}
    html:has(#eden-dark-chk:checked) .ceo-summary{background:linear-gradient(90deg,rgba(99,102,241,.1),transparent)!important}
    html:has(#eden-dark-chk:checked) .report-section-title{border-bottom-color:rgba(99,102,241,.2)!important}
    html:has(#eden-dark-chk:checked) .rpt-row{border-bottom-color:rgba(255,255,255,.06)!important}
    html:has(#eden-dark-chk:checked) .verdict-box{background:linear-gradient(135deg,#1e1e3a,#1a1a2e)!important;border-color:rgba(99,102,241,.3)!important}
    html:has(#eden-dark-chk:checked) .price-bar-track{background:#2d2d4e!important}
    html:has(#eden-dark-chk:checked) .company-full,
    html:has(#eden-dark-chk:checked) .analyst-sub,
    html:has(#eden-dark-chk:checked) .news-meta,
    html:has(#eden-dark-chk:checked) .verdict-meta{color:#9ca3af!important}
    html:has(#eden-dark-chk:checked) [data-testid="stTabs"] [role="tab"]{color:#9ca3af!important}
    html:has(#eden-dark-chk:checked) [data-testid="stTabs"] [role="tab"][aria-selected="true"]{color:#a78bfa!important}
    html:has(#eden-dark-chk:checked) .peers-add{background:rgba(99,102,241,.08)!important;border-color:rgba(99,102,241,.35)!important}
    html:has(#eden-dark-chk:checked) #eden-panel{background:#1a1a2e!important;border-color:rgba(99,102,241,.3)!important}
    html:has(#eden-dark-chk:checked) .eden-panel-item{color:#e2e2f0!important}
    html:has(#eden-dark-chk:checked) #eden-dots-btn{background:rgba(26,26,46,.92)!important;border-color:rgba(167,139,250,.5)!important}
    </style>
    """, unsafe_allow_html=True)

    # HTML only — no <script> (Streamlit would render script content as visible text)
    _auth_href = "/_stauth/logout" if is_logged_in else "https://accounts.google.com"
    _auth_label = (
        f'&#128682; Sign Out ({account_label.replace("&#128100; ", "")})' if is_logged_in
        else '&#128100; Sign in with Google'
    )
    _auth_color = "#ef4444" if is_logged_in else "#6366f1"
    st.markdown(f"""
    <input type="checkbox" id="eden-menu-chk" style="position:fixed;opacity:0;pointer-events:none;top:-9999px">
    <input type="checkbox" id="eden-dark-chk" style="position:fixed;opacity:0;pointer-events:none;top:-9999px">
    <label for="eden-menu-chk" id="eden-menu-backdrop"></label>
    <label for="eden-menu-chk" id="eden-dots-btn" title="Settings">&#8942;</label>
    <div id="eden-panel">
      <div class="eden-panel-title">Settings</div>
      <label for="eden-dark-chk" class="eden-panel-item">
        <span>&#127769; Dark Mode</span>
        <div class="eden-toggle"><div class="eden-toggle-knob"></div></div>
      </label>
      <div class="eden-panel-sep"></div>
      <a href="{_auth_href}" class="eden-panel-item"
         style="text-decoration:none;cursor:pointer;color:{_auth_color};display:flex;align-items:center;">
        <span>{_auth_label}</span>
      </a>
      <div class="eden-panel-sep"></div>
      <div class="eden-panel-item" style="color:#6b7280;font-size:11px;cursor:default">
        <span>Eden Sovereign v1.0</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # JavaScript via components (executes in iframe, accesses parent DOM for localStorage)
    st.components.v1.html("""
    <script>
    (function(){
        function tryInit() {
            var doc = window.parent.document;
            var darkChk = doc.getElementById('eden-dark-chk');
            if (!darkChk) { setTimeout(tryInit, 100); return; }
            if (darkChk._lsBound) return;
            darkChk._lsBound = true;
            var saved = window.parent.localStorage.getItem('eden-dark') === '1';
            darkChk.checked = saved;
            darkChk.addEventListener('change', function() {
                window.parent.localStorage.setItem('eden-dark', this.checked ? '1' : '0');
            });
        }
        tryInit();
    })();
    </script>
    """, height=0)


# ── Helpers ───────────────────────────────────────────────────────────────────
def _safe(val, fallback=float("nan")):
    if val is None:
        return fallback
    try:
        if np.isnan(float(val)):
            return fallback
    except (TypeError, ValueError):
        pass
    return val

def _isnan(v) -> bool:
    try: return np.isnan(float(v))
    except: return True

def fmt_mcap(mc: float) -> str:
    if mc >= 1e12: return f"${mc/1e12:.2f}T"
    if mc >= 1e9:  return f"${mc/1e9:.1f}B"
    if mc >= 1e6:  return f"${mc/1e6:.1f}M"
    return f"${mc:,.0f}"

def fmt_pct(v: float, dec: int = 1) -> str:
    return "N/A" if _isnan(v) else f"{v*100:.{dec}f}%"

def fmt_price(v: float) -> str:
    return "N/A" if _isnan(v) or v == 0 else f"${v:,.2f}"


# ── Data Fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=180, show_spinner=False)
def fetch_data(ticker: str) -> dict:
    out: dict = {
        "ticker": ticker, "info": {}, "hist": pd.DataFrame(),
        "company_name": ticker, "current_price": float("nan"),
        "prev_close": float("nan"), "mkt_cap": 0.0,
        "pe_ratio": float("nan"), "forward_pe": float("nan"),
        "peg_ratio": float("nan"), "gross_margins": float("nan"),
        "fcf": float("nan"), "revenue_cagr": 0.0,
        "fcf_yield": float("nan"), "sector": "N/A", "dividend_yield": 0.0,
        "week52_high": float("nan"), "week52_low": float("nan"),
        "analyst_target_mean": float("nan"), "analyst_target_high": float("nan"),
        "analyst_target_low": float("nan"), "analyst_target_median": float("nan"),
        "n_analysts": 0, "rec_mean": float("nan"), "rec_key": "N/A",
        "error": None,
        "is_etf": False, "quote_type": "EQUITY",
    }
    import time as _time
    try:
        obj = yf.Ticker(ticker)
        # ── obj.info with retry on rate-limit ────────────────────────────────
        info = {}
        for _attempt in range(3):
            try:
                info = obj.info or {}
                break
            except Exception as _e:
                _emsg = str(_e).lower()
                if ("too many requests" in _emsg or "rate limit" in _emsg or "429" in _emsg) \
                        and _attempt < 2:
                    _time.sleep(3 * (2 ** _attempt))  # 3s → 6s → 12s
                    continue
                break  # non-rate-limit error — give up
        out["info"] = info

        # ── fast_info (always works — cached separately by yfinance) ──────────
        try:
            fi = obj.fast_info
        except Exception:
            fi = {}

        def _fi(key, fallback=None):
            """Read from fast_info safely (dict-like or attribute-like)."""
            try:
                v = fi[key] if hasattr(fi, "__getitem__") else getattr(fi, key, None)
                return v if v not in (None, float("nan")) else fallback
            except Exception:
                return fallback

        out["company_name"]  = info.get("longName") or info.get("shortName") or ticker
        qt = info.get("quoteType") or str(_fi("quoteType", "EQUITY"))
        qt = qt.upper() if qt else "EQUITY"
        out["quote_type"] = qt
        out["is_etf"]     = qt in ("ETF", "MUTUALFUND", "INDEX")

        # Price: info → fast_info → history (filled later)
        _price = (info.get("currentPrice") or info.get("regularMarketPrice")
                  or info.get("navPrice") or info.get("ask") or info.get("bid")
                  or _fi("last_price"))
        out["current_price"] = float(_safe(_price, float("nan")))

        _prev = (info.get("previousClose") or info.get("regularMarketPreviousClose")
                 or _fi("previous_close") or _fi("regular_market_previous_close"))
        out["prev_close"] = float(_safe(_prev, float("nan")))

        # Market cap: info → fast_info
        _mc = info.get("marketCap") or _fi("market_cap")
        out["mkt_cap"] = float(_safe(_mc, 0.0))

        out["pe_ratio"]      = float(_safe(info.get("trailingPE"), float("nan")))
        out["forward_pe"]    = float(_safe(info.get("forwardPE"), float("nan")))
        out["gross_margins"] = float(_safe(info.get("grossMargins"), float("nan")))
        out["fcf"]           = float(_safe(info.get("freeCashflow"), float("nan")))

        # ── Fetch all financial statements ONCE with retry ─────────────────
        # Prevents duplicate calls and cascading rate-limits
        def _stmt_fetch(primary: str, fallback: str | None = None):
            for _a in range(3):
                try:
                    _v = getattr(obj, primary, None)
                    if _v is not None and not (hasattr(_v, "empty") and _v.empty):
                        return _v
                    if fallback:
                        _v2 = getattr(obj, fallback, None)
                        if _v2 is not None and not (hasattr(_v2, "empty") and _v2.empty):
                            return _v2
                    return _v  # even if empty, stop retrying
                except Exception as _se:
                    _sm = str(_se).lower()
                    if ("too many requests" in _sm or "429" in _sm or "rate limit" in _sm) \
                            and _a < 2:
                        _time.sleep(3 * (2 ** _a))
                        continue
                    return None
            return None

        _ann_income = _stmt_fetch("income_stmt", "financials")       # annual income stmt
        _q_income   = _stmt_fetch("quarterly_income_stmt", "quarterly_financials")
        _cf_stmt    = _stmt_fetch("cashflow", "cash_flow")            # annual cash flow
        _ann_fin    = _ann_income  # same data; reuse

        # ── P/E fallback: multiple sources ───────────────────────────────────
        if _isnan(out["pe_ratio"]):
            try:
                # Source 2: trailingEps / epsTrailingTwelveMonths from info
                _eps = info.get("trailingEps") or info.get("epsTrailingTwelveMonths")
                _px  = out["current_price"]
                if _eps and not _isnan(float(_eps)) and float(_eps) != 0 \
                        and not _isnan(_px) and _px > 0:
                    out["pe_ratio"] = float(_px) / float(_eps)
            except Exception:
                pass
        if _isnan(out["pe_ratio"]):
            try:
                # Source 3: TTM EPS from quarterly income stmt (sum last 4 quarters)
                if _q_income is not None and not _q_income.empty:
                    for _lbl in ["Basic EPS", "Diluted EPS"]:
                        if _lbl in _q_income.index:
                            _eps_s = _q_income.loc[_lbl].dropna().sort_index(ascending=False)
                            if len(_eps_s) >= 4:
                                _ttm_eps = float(_eps_s.iloc[:4].sum())
                                _px = out["current_price"]
                                if _ttm_eps != 0 and not _isnan(_px) and _px > 0:
                                    out["pe_ratio"] = float(_px) / _ttm_eps
                            break
            except Exception:
                pass
        if _isnan(out["pe_ratio"]):
            try:
                # Source 4: Market Cap ÷ Net Income
                _ni  = info.get("netIncomeToCommon") or info.get("netIncome")
                _mc4 = out["mkt_cap"]
                if _ni and not _isnan(float(_ni)) and float(_ni) > 0 and _mc4 > 0:
                    out["pe_ratio"] = _mc4 / float(_ni)
            except Exception:
                pass
        if _isnan(out["pe_ratio"]):
            try:
                # Source 5: annual income statement EPS or Net Income ÷ shares
                if _ann_income is not None and not _ann_income.empty:
                    for _lbl5 in ["Basic EPS", "Diluted EPS", "Net Income"]:
                        if _lbl5 in _ann_income.index:
                            _v5 = _ann_income.loc[_lbl5].dropna().sort_index(ascending=False)
                            if not _v5.empty:
                                _val5 = float(_v5.iloc[0])
                                _px5  = out["current_price"]
                                if _lbl5.endswith("EPS") and _val5 != 0 \
                                        and not _isnan(_px5) and _px5 > 0:
                                    out["pe_ratio"] = _px5 / _val5
                                    break
                                elif _lbl5 == "Net Income" and _val5 > 0:
                                    _shr = info.get("sharesOutstanding") \
                                           or info.get("impliedSharesOutstanding")
                                    if _shr and float(_shr) > 0 \
                                            and not _isnan(_px5) and _px5 > 0:
                                        out["pe_ratio"] = _px5 / (_val5 / float(_shr))
                                        break
            except Exception:
                pass

        # ── Forward P/E fallback ───────────────────────────────────────────
        if _isnan(out["forward_pe"]):
            try:
                _feps = info.get("forwardEps")
                _px   = out["current_price"]
                if _feps and not _isnan(float(_feps)) and float(_feps) > 0 \
                        and not _isnan(_px) and _px > 0:
                    out["forward_pe"] = float(_px) / float(_feps)
            except Exception:
                pass

        # ── FCF fallback: Operating Cash Flow − CapEx ─────────────────────
        if _isnan(out["fcf"]):
            try:
                if _cf_stmt is not None and not _cf_stmt.empty:
                    _ocf, _capex = None, None
                    for _lbl in ["Operating Cash Flow", "Total Cash From Operating Activities"]:
                        if _lbl in _cf_stmt.index:
                            _ocf = float(_cf_stmt.loc[_lbl].dropna().iloc[0])
                            break
                    for _lbl in ["Capital Expenditure", "Capital Expenditures"]:
                        if _lbl in _cf_stmt.index:
                            _capex = float(_cf_stmt.loc[_lbl].dropna().iloc[0])
                            break
                    if _ocf is not None:
                        out["fcf"] = _ocf + (_capex if _capex is not None else 0.0)
            except Exception:
                pass

        # ── Gross margins fallback from income statement ───────────────────
        if _isnan(out["gross_margins"]):
            try:
                if _ann_income is not None and not _ann_income.empty:
                    if "Gross Profit" in _ann_income.index:
                        for _tr_lbl in ["Total Revenue", "Revenue"]:
                            if _tr_lbl in _ann_income.index:
                                _gp = _ann_income.loc["Gross Profit"].dropna()
                                _tr = _ann_income.loc[_tr_lbl].dropna()
                                if not _gp.empty and not _tr.empty \
                                        and float(_tr.iloc[0]) > 0:
                                    out["gross_margins"] = \
                                        float(_gp.iloc[0]) / float(_tr.iloc[0])
                                break
            except Exception:
                pass

        out["sector"]         = info.get("sector") or "N/A"
        out["dividend_yield"] = float(_safe(info.get("dividendYield"), 0.0))

        # 52-week range: info → fast_info
        _52h = info.get("fiftyTwoWeekHigh") or _fi("year_high")
        _52l = info.get("fiftyTwoWeekLow")  or _fi("year_low")
        out["week52_high"] = float(_safe(_52h, float("nan")))
        out["week52_low"]  = float(_safe(_52l, float("nan")))

        # ── Market cap fallback: shares × price ───────────────────────────
        if out["mkt_cap"] == 0.0:
            try:
                _shr_mc = info.get("sharesOutstanding") \
                          or info.get("impliedSharesOutstanding") \
                          or _fi("shares")
                _px_mc  = out["current_price"]
                if _shr_mc and float(_shr_mc) > 0 and not _isnan(_px_mc) and _px_mc > 0:
                    out["mkt_cap"] = float(_shr_mc) * float(_px_mc)
            except Exception:
                pass

        # ── Analyst data: info → fallback keys ────────────────────────────
        out["analyst_target_mean"]   = float(_safe(
            info.get("targetMeanPrice") or info.get("targetPrice"), float("nan")))
        out["analyst_target_high"]   = float(_safe(
            info.get("targetHighPrice"), float("nan")))
        out["analyst_target_low"]    = float(_safe(
            info.get("targetLowPrice"), float("nan")))
        out["analyst_target_median"] = float(_safe(
            info.get("targetMedianPrice") or info.get("targetMeanPrice"), float("nan")))
        out["n_analysts"]            = int(_safe(
            info.get("numberOfAnalystOpinions") or info.get("numAnalystOpinions"), 0))
        out["rec_mean"]              = float(_safe(
            info.get("recommendationMean"), float("nan")))
        out["rec_key"]               = (info.get("recommendationKey")
                                        or info.get("averageAnalystRating") or "N/A")

        # ── FCF Yield ──────────────────────────────────────────────────────
        if out["mkt_cap"] > 0 and not _isnan(out["fcf"]):
            out["fcf_yield"] = out["fcf"] / out["mkt_cap"]

        # ── Revenue CAGR (annual, then quarterly fallback) ─────────────────
        try:
            if _ann_fin is not None and not _ann_fin.empty:
                for lbl in ["Total Revenue", "Revenue"]:
                    if lbl in _ann_fin.index:
                        rev = _ann_fin.loc[lbl].dropna().sort_index()
                        if len(rev) >= 3:
                            oldest, latest, n = float(rev.iloc[0]), float(rev.iloc[-1]), len(rev)-1
                            if oldest > 0 and latest > 0:
                                out["revenue_cagr"] = float((latest/oldest)**(1.0/n) - 1.0)
                        elif len(rev) == 2:
                            oldest, latest = float(rev.iloc[0]), float(rev.iloc[-1])
                            if oldest > 0 and latest > 0:
                                out["revenue_cagr"] = float((latest/oldest - 1.0) * 0.6)
                        break
        except Exception:
            pass

        if out["revenue_cagr"] == 0.0:
            try:
                if _q_income is not None and not _q_income.empty:
                    for lbl in ["Total Revenue", "Revenue"]:
                        if lbl in _q_income.index:
                            qrev = _q_income.loc[lbl].dropna().sort_index()
                            if len(qrev) >= 4:
                                _recent = float(qrev.iloc[-4:].sum())
                                _prior  = float(qrev.iloc[-8:-4].sum()) \
                                          if len(qrev) >= 8 else float(qrev.iloc[:4].sum())
                                if _prior > 0 and _recent > 0:
                                    out["revenue_cagr"] = float((_recent/_prior - 1.0) * 0.7)
                            break
            except Exception:
                pass

        # ── PEG ratio: forward-first approach ─────────────────────────────
        def _cap_growth(g_raw: float) -> float:
            return float(np.clip(g_raw, 0.05, 0.40))

        peg = None
        _pg1 = _safe(info.get("pegRatio"), None)
        if _pg1 is not None and not _isnan(float(_pg1)) and float(_pg1) > 0:
            peg = float(_pg1)

        if peg is None or _isnan(float(peg)):
            try:
                _ltg  = info.get("longTermGrowth") or info.get("longTermEpsGrowthRate")
                _fpe2 = out["forward_pe"] if not _isnan(out["forward_pe"]) else None
                if _fpe2 and _ltg and float(_fpe2) > 0 and float(_ltg) > 0:
                    peg = float(_fpe2) / (_cap_growth(float(_ltg)) * 100.0)
            except Exception:
                pass

        if peg is None or _isnan(float(peg)):
            _pg3 = _safe(info.get("trailingPegRatio"), None)
            if _pg3 is not None and not _isnan(float(_pg3)) and 0 < float(_pg3) < 10:
                peg = float(_pg3)

        if peg is None or _isnan(float(peg)):
            try:
                _fpe4 = out["forward_pe"] if not _isnan(out["forward_pe"]) \
                        else info.get("forwardPE")
                _eg4  = info.get("earningsGrowth")
                if _fpe4 and _eg4 and float(_fpe4) > 0 and float(_eg4) > 0:
                    peg = float(_fpe4) / (_cap_growth(float(_eg4)) * 100.0)
            except Exception:
                pass

        if peg is None or _isnan(float(peg)):
            try:
                _pe5  = out["pe_ratio"]
                _eqg5 = info.get("earningsQuarterlyGrowth")
                if _pe5 and _eqg5 and not _isnan(float(_pe5)) and float(_pe5) > 0 \
                        and float(_eqg5) > 0:
                    peg = float(_pe5) / (_cap_growth(float(_eqg5)) * 100.0)
            except Exception:
                pass

        if peg is None or _isnan(float(peg)):
            try:
                _pe6 = out["pe_ratio"]
                if not _isnan(_pe6) and float(_pe6) > 0 \
                        and _ann_income is not None and not _ann_income.empty:
                    for _lbl6 in ["Basic EPS", "Diluted EPS"]:
                        if _lbl6 in _ann_income.index:
                            _eps6 = _ann_income.loc[_lbl6].dropna().sort_index()
                            if len(_eps6) >= 2:
                                _e_old6, _e_new6 = float(_eps6.iloc[0]), float(_eps6.iloc[-1])
                                _n6 = len(_eps6) - 1
                                if _e_old6 > 0 and _e_new6 > 0:
                                    _eps_cagr6 = (_e_new6/_e_old6)**(1.0/_n6) - 1.0
                                    if _eps_cagr6 > 0.01:
                                        peg = float(_pe6) / (_cap_growth(_eps_cagr6) * 100.0)
                            break
            except Exception:
                pass

        if peg is None or _isnan(float(peg)):
            try:
                _pe7, _rcagr = out["pe_ratio"], out["revenue_cagr"]
                if not _isnan(_pe7) and float(_pe7) > 0 \
                        and not _isnan(_rcagr) and float(_rcagr) > 0.02:
                    peg = float(_pe7) / (_cap_growth(float(_rcagr)) * 100.0)
            except Exception:
                pass

        out["peg_ratio"] = float(_safe(peg, float("nan")))

        # ── Historical prices (with retry + yf.download fallback) ────────────
        _hist_ok = False
        for _ha in range(3):
            try:
                hist = obj.history(period="1y", interval="1d", auto_adjust=True)
                hist = hist.dropna(subset=["Close"])
                if hist.empty:
                    hist = obj.history(
                        start=(datetime.today()-timedelta(days=400)).strftime("%Y-%m-%d"),
                        end=datetime.today().strftime("%Y-%m-%d"),
                        interval="1d", auto_adjust=True).dropna(subset=["Close"])
                if not hist.empty:
                    out["hist"] = hist
                    _hist_ok = True
                    break
            except Exception as _he:
                _hmsg = str(_he).lower()
                if ("too many requests" in _hmsg or "429" in _hmsg or "rate limit" in _hmsg) \
                        and _ha < 2:
                    _time.sleep(4 * (2 ** _ha))  # 4s → 8s → 16s
                    continue
                break

        # Final fallback: yf.download (different endpoint, less rate-limited)
        if not _hist_ok or out["hist"].empty:
            try:
                _dl = yf.download(
                    ticker, period="1y", interval="1d",
                    auto_adjust=True, progress=False, threads=False,
                )
                if _dl is not None and not _dl.empty:
                    _dl = _dl.dropna(subset=["Close"])
                    out["hist"] = _dl
                    _hist_ok = True
            except Exception:
                pass

        hist = out["hist"]
        if not hist.empty:
            if _isnan(out["current_price"]):
                out["current_price"] = float(hist["Close"].iloc[-1])
            if _isnan(out["prev_close"]) and len(hist) >= 2:
                out["prev_close"] = float(hist["Close"].iloc[-2])
        elif not _hist_ok:
            out["error"] = out.get("error") or "Rate limited. Try after a while."

    except Exception as e:
        out["error"] = str(e)
    return out


# ── Technical Indicators ──────────────────────────────────────────────────────
def compute_technicals(df: pd.DataFrame) -> dict:
    nan = float("nan")
    empty = pd.Series(dtype=float)
    tech = {
        "ma50": nan, "ma150": nan, "ma200": nan,
        "rsi": 50.0, "macd_hist": 0.0,
        "ma50_series": empty, "ma150_series": empty, "ma200_series": empty,
        "rsi_series": empty,
        "macd_line": empty, "macd_signal": empty, "macd_hist_series": empty,
        "bb_upper": empty, "bb_lower": empty, "bb_mid": empty,
        "stoch_k": empty, "stoch_d": empty,
        "obv": empty, "atr": empty, "vwap": empty,
    }
    if df.empty or len(df) < 14:
        return tech

    close = df["Close"].astype(float)
    high  = df["High"].astype(float)
    low   = df["Low"].astype(float)
    vol   = df["Volume"].astype(float)

    # Moving Averages
    for period, key in [(50, "ma50"), (150, "ma150"), (200, "ma200")]:
        s = close.rolling(period, min_periods=1).mean()
        tech[f"{key}_series"] = s
        tech[key] = float(s.iloc[-1]) if not s.empty else nan

    # RSI-14 (full series)
    try:
        delta = close.diff()
        gain  = delta.clip(lower=0).rolling(14, min_periods=14).mean()
        loss  = (-delta).clip(lower=0).rolling(14, min_periods=14).mean()
        rs    = gain / loss.replace(0, float("nan"))
        rsi_s = 100.0 - 100.0 / (1.0 + rs)
        tech["rsi_series"] = rsi_s
        tech["rsi"] = float(rsi_s.dropna().iloc[-1]) if not rsi_s.dropna().empty else 50.0
    except Exception:
        pass

    # MACD (12, 26, 9) — full series
    try:
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd_line   = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        hist_series = macd_line - signal_line
        tech["macd_line"]        = macd_line
        tech["macd_signal"]      = signal_line
        tech["macd_hist_series"] = hist_series
        tech["macd_hist"]        = float(hist_series.iloc[-1]) if not hist_series.empty else 0.0
    except Exception:
        pass

    # Bollinger Bands (20, 2)
    try:
        sma20 = close.rolling(20, min_periods=1).mean()
        std20 = close.rolling(20, min_periods=1).std()
        tech["bb_mid"]   = sma20
        tech["bb_upper"] = sma20 + 2.0 * std20
        tech["bb_lower"] = sma20 - 2.0 * std20
    except Exception:
        pass

    # Stochastic (14, 3)
    try:
        low14  = low.rolling(14, min_periods=1).min()
        high14 = high.rolling(14, min_periods=1).max()
        denom  = (high14 - low14).replace(0, float("nan"))
        k = 100.0 * (close - low14) / denom
        d = k.rolling(3, min_periods=1).mean()
        tech["stoch_k"] = k
        tech["stoch_d"] = d
    except Exception:
        pass

    # OBV
    try:
        direction = np.where(close > close.shift(1), 1.0,
                    np.where(close < close.shift(1), -1.0, 0.0))
        obv = pd.Series(direction * vol.values, index=df.index).cumsum()
        tech["obv"] = obv
    except Exception:
        pass

    # ATR (14)
    try:
        hl  = high - low
        hpc = (high - close.shift(1)).abs()
        lpc = (low  - close.shift(1)).abs()
        tr  = pd.concat([hl, hpc, lpc], axis=1).max(axis=1)
        tech["atr"] = tr.rolling(14, min_periods=1).mean()
    except Exception:
        pass

    # VWAP (running, from start of fetched period)
    try:
        typical = (high + low + close) / 3.0
        tech["vwap"] = (typical * vol).cumsum() / vol.cumsum()
    except Exception:
        pass

    return tech


def compute_ma_series(df: pd.DataFrame, period: int) -> pd.Series:
    if df.empty or period < 1:
        return pd.Series(dtype=float)
    return df["Close"].astype(float).rolling(period, min_periods=1).mean()


# ── News Sentiment Score (via stock-analysis skill) ───────────────────────────
_SKILL_SCRIPT = os.path.join(
    os.path.dirname(__file__),
    ".agents", "skills", "stock-analysis", "scripts", "analyze_stock.py"
)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_news_score(ticker: str) -> float:
    """
    Calls the stock-analysis skill script and returns a sentiment score 0.0–1.0.
    Returns 0.5 (neutral) on any failure.
    """
    import subprocess, sys
    try:
        result = subprocess.run(
            [sys.executable, "-m", "uv", "run", _SKILL_SCRIPT, ticker, "--output", "json"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            # Find the JSON object in stdout (may have install noise before it)
            _txt = result.stdout
            _start = _txt.find("{")
            if _start != -1:
                _data = json.loads(_txt[_start:])
                _s = float(_data.get("final_score", 0.5))
                return float(np.clip(_s, 0.0, 1.0))
    except Exception:
        pass
    return 0.5  # neutral fallback


# ── Quantum Scoring Engine ────────────────────────────────────────────────────
def compute_score(data: dict, tech: dict, horizon: str, use_news: bool = True) -> int:
    price   = np.float64(_safe(data["current_price"], 100.0))
    rsi     = np.float64(tech["rsi"])
    macd    = np.float64(tech["macd_hist"])

    # MA50: if missing, give neutral 5/10 (not full 10/10)
    _ma50_raw = tech.get("ma50")
    _ma50_missing = _ma50_raw is None or _isnan(float(_ma50_raw))
    ma50v = np.float64(float(price) if _ma50_missing else float(_ma50_raw))

    pe      = np.float64(data["pe_ratio"])
    peg     = np.float64(data["peg_ratio"])

    # margins/fcf: NaN if missing — never assume a default value
    _margins_raw = data["gross_margins"]
    _margins_missing = _isnan(float(_safe(_margins_raw, float("nan"))))
    margins = np.float64(float(_safe(_margins_raw, 0.0)))

    cagr    = np.float64(data["revenue_cagr"])

    _fcfy_raw = data["fcf_yield"]
    _fcfy_missing = _isnan(float(_safe(_fcfy_raw, float("nan"))))
    fcfy    = np.float64(float(_safe(_fcfy_raw, 0.0)))

    total = np.float64(0.0)

    if horizon == "30D Tactical":
        # RSI (max 35) — wide range 20-80 for fairness
        rsi_score = np.float64(np.clip((float(rsi)-20.0)/60.0*35.0, 0.0, 35.0))
        if float(rsi) > 75.0: rsi_score = np.float64(max(0.0, float(rsi_score)-8.0))
        if float(rsi) < 25.0: rsi_score = np.float64(max(0.0, float(rsi_score)-5.0))

        # MACD (max 20) — normalize by 1% of price to handle all price levels
        denom      = np.float64(max(abs(float(price)*0.01), 1e-9))
        macd_norm  = np.float64(np.clip(float(macd)/float(denom), -1.0, 1.0))
        macd_score = np.float64(10.0 + macd_norm*10.0)

        # MA50 trend (max 10) — neutral 5 if MA50 unavailable
        if _ma50_missing:
            ma_score = np.float64(5.0)
        elif float(price) >= float(ma50v):
            ma_score = np.float64(10.0)
        else:
            below = (float(ma50v)-float(price))/max(float(ma50v),1e-9)
            ma_score = np.float64(max(0.0, 10.0 - below*120.0))

        # P/E (max 15) — neutral 4 if missing (below average, not free points)
        if _isnan(float(pe)) or float(pe) <= 0:
            pe_score = np.float64(4.0)
        elif float(pe) < 20:   pe_score = np.float64(15.0)
        elif float(pe) < 35:   pe_score = np.float64(15.0-(float(pe)-20.0)/15.0*7.0)
        elif float(pe) < 60:   pe_score = np.float64(8.0-(float(pe)-35.0)/25.0*5.0)
        else:                  pe_score = np.float64(3.0)

        # PEG (max 10) — neutral 3 if missing
        if _isnan(float(peg)) or float(peg) <= 0:
            peg_score = np.float64(3.0)
        else:
            peg_score = np.float64(np.clip((3.0-float(peg))/3.0*10.0, 0.0, 10.0))

        # CAGR bonus (max 10, penalty for negative CAGR)
        _cagr_clipped = float(np.clip(float(cagr), -0.30, 0.30))
        cagr_bonus = np.float64(_cagr_clipped / 0.30 * 10.0)
        cagr_bonus = np.float64(np.clip(float(cagr_bonus), -5.0, 10.0))

        total = rsi_score + macd_score + ma_score + pe_score + peg_score + cagr_bonus
        # No mega-cap floor guarantee — let each stock earn its score

    else:  # 1Y Strategic
        # CAGR (max 25, penalty for negative CAGR down to -8)
        _cagr_clipped = float(np.clip(float(cagr), -0.30, 0.30))
        cagr_score = np.float64(np.clip(_cagr_clipped / 0.30 * 25.0, -8.0, 25.0))

        # PEG (max 20) — neutral 5 if missing (not 8)
        if _isnan(float(peg)) or float(peg) <= 0:
            peg_score = np.float64(5.0)
        else:
            peg_score = np.float64(np.clip((3.0-float(peg))/3.0*20.0, 0.0, 20.0))
            # No extra PEG double bonus — peg_score already rewards low PEG

        # FCF yield (max 20) — 0 if missing (not free points)
        if _fcfy_missing:
            fcf_score = np.float64(0.0)
        else:
            fcf_score = np.float64(np.clip(float(fcfy)/0.08*20.0, 0.0, 20.0))

        # Gross margins (max 15) — 0 if missing
        if _margins_missing:
            margin_score = np.float64(0.0)
        else:
            margin_score = np.float64(np.clip(float(margins)/0.40*15.0, 0.0, 15.0))

        tech_score   = np.float64(np.clip((float(rsi)-20.0)/60.0*20.0, 0.0, 20.0))
        total = cagr_score + peg_score + fcf_score + margin_score + tech_score
        # No mega-cap floor guarantee

    # ── News Sentiment overlay (only for single-ticker analysis, not batch scans) ──
    # 30D: news = 15% weight  |  1Y: news = 5% weight
    if use_news:
        try:
            _news_raw = fetch_news_score(data["ticker"])
            _news_weight = 0.15 if horizon == "30D Tactical" else 0.05
            total = float(total) * (1.0 - _news_weight) + _news_raw * 100.0 * _news_weight
        except Exception:
            pass  # If news fetch fails, use base score unchanged

    return int(np.clip(float(total), 1.0, 100.0))


# ── Portfolio persistence helpers ─────────────────────────────────────────────
_PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), "portfolio_state.json")


def _save_portfolio(portfolio: list) -> None:
    # אם משתמש מחובר דרך טלגרם — שמור בחשבון שלו
    try:
        _cu = st.session_state.get("current_user_phone", "")
        if _cu:
            _save_user_portfolio(_cu, portfolio)
            return
    except Exception:
        pass
    # fallback — קובץ מקומי
    try:
        with open(_PORTFOLIO_FILE, "w", encoding="utf-8") as _f:
            json.dump(portfolio, _f)
    except Exception:
        pass


def _load_portfolio() -> list:
    # אם משתמש מחובר דרך טלגרם — טען מחשבון שלו
    try:
        _cu = st.session_state.get("current_user_phone", "")
        if _cu:
            return _load_user_portfolio(_cu)
    except Exception:
        pass
    # fallback — קובץ מקומי
    try:
        if os.path.exists(_PORTFOLIO_FILE):
            with open(_PORTFOLIO_FILE, "r", encoding="utf-8") as _f:
                data = json.load(_f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


# ── Telegram Price Alerts ──────────────────────────────────────────────────────
_ALERTS_FILE = os.path.join(os.path.dirname(__file__), "telegram_chats.json")


def _normalize_phone(phone: str) -> str:
    import re as _re
    digits = _re.sub(r"\D", "", phone)
    if digits.startswith("00"):
        return digits[2:]
    if digits.startswith("0"):
        return "972" + digits[1:]
    return digits


def _load_alerts_db() -> dict:
    try:
        if os.path.exists(_ALERTS_FILE):
            data = json.load(open(_ALERTS_FILE, encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("registrations", {})
                data.setdefault("alerts", [])
                data.setdefault("_last_poll", None)
                return data
    except Exception:
        pass
    return {"registrations": {}, "alerts": [], "_last_poll": None}


def _save_alerts_db(db: dict) -> None:
    try:
        json.dump(db, open(_ALERTS_FILE, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    except Exception:
        pass


def _tg_token() -> str:
    return st.secrets.get("TELEGRAM_BOT_TOKEN", "")


def _poll_telegram_registrations() -> int:
    """קורא עדכונים מהבוט ורושם מספרי טלפון שנשלחו דרך /start"""
    import requests as _req, re as _re
    try:
        token = _tg_token()
        if not token:
            return 0
        db = _load_alerts_db()
        # throttle: לא יותר מפעם אחת ב-30 שניות
        if db["_last_poll"]:
            elapsed = (datetime.now() - datetime.fromisoformat(db["_last_poll"])).total_seconds()
            if elapsed < 30:
                return 0
        resp = _req.get(
            f"https://api.telegram.org/bot{token}/getUpdates",
            params={"offset": -100, "limit": 100},
            timeout=8,
        )
        if not resp.ok:
            return 0
        new = 0
        for upd in resp.json().get("result", []):
            msg = upd.get("message", {})
            text = (msg.get("text") or "").strip()
            chat_id = msg.get("chat", {}).get("id")
            if not text or not chat_id:
                continue
            m = _re.match(r"^/start\s+([\d\s\-\+]+)$", text, _re.I)
            if not m:
                continue
            norm = _normalize_phone(m.group(1))
            if len(norm) >= 7 and norm not in db["registrations"]:
                db["registrations"][norm] = {
                    "chat_id": chat_id,
                    "registered_at": datetime.now().isoformat(timespec="seconds"),
                    "display_phone": m.group(1).strip(),
                }
                new += 1
        db["_last_poll"] = datetime.now().isoformat(timespec="seconds")
        _save_alerts_db(db)
        return new
    except Exception:
        return 0


def _send_telegram_msg(phone: str, text: str) -> bool:
    import requests as _req
    try:
        token = _tg_token()
        if not token:
            return False
        db = _load_alerts_db()
        reg = db["registrations"].get(_normalize_phone(phone), {})
        chat_id = reg.get("chat_id")
        if not chat_id:
            return False
        r = _req.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=8,
        )
        return r.ok
    except Exception:
        return False


def _is_phone_registered(phone: str) -> bool:
    return _normalize_phone(phone) in _load_alerts_db().get("registrations", {})


def _add_tg_alert(phone: str, ticker: str, condition: str, target_price: float) -> bool:
    try:
        if not _is_phone_registered(phone):
            return False
        db = _load_alerts_db()
        db["alerts"].append({
            "phone": _normalize_phone(phone),
            "ticker": ticker.upper(),
            "condition": condition,
            "target_price": float(target_price),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "triggered": False,
            "last_checked": None,
        })
        _save_alerts_db(db)
        return True
    except Exception:
        return False


def _list_tg_alerts(phone: str) -> list:
    norm = _normalize_phone(phone)
    return [a for a in _load_alerts_db().get("alerts", []) if a.get("phone") == norm]


def _delete_tg_alert(phone: str, idx: int) -> None:
    norm = _normalize_phone(phone)
    db = _load_alerts_db()
    user_idxs = [i for i, a in enumerate(db["alerts"]) if a.get("phone") == norm]
    if 0 <= idx < len(user_idxs):
        db["alerts"].pop(user_idxs[idx])
        _save_alerts_db(db)


def _check_and_fire_tg_alerts(current_prices: dict) -> int:
    try:
        db = _load_alerts_db()
        fired = 0
        changed = False
        for alert in db.get("alerts", []):
            if alert.get("triggered"):
                continue
            price = current_prices.get(alert["ticker"])
            if not price:
                continue
            target = float(alert["target_price"])
            hit = (
                (alert["condition"] == "above" and price >= target) or
                (alert["condition"] == "below" and price <= target) or
                (alert["condition"] == "equals" and abs(price - target) / target <= 0.005)
            )
            alert["last_checked"] = datetime.now().isoformat(timespec="seconds")
            changed = True
            if hit:
                direction = "עלה מעל" if alert["condition"] == "above" else ("הגיע ל" if alert["condition"] == "equals" else "ירד מתחת")
                body = (
                    f"🔔 *Eden Sovereign — התראת מחיר*\n\n"
                    f"מניה: *{alert['ticker']}*\n"
                    f"{direction} יעד ${target:,.2f}\n"
                    f"מחיר נוכחי: *${price:,.2f}*"
                )
                ok = _send_telegram_msg(alert["phone"], body)
                if ok:
                    alert["triggered"] = True
                    fired += 1
        if changed:
            _save_alerts_db(db)
        return fired
    except Exception:
        return 0


def _load_user_portfolio(phone: str) -> list:
    """טוען את ה-Portfolio מחשבון הטלגרם של המשתמש"""
    try:
        norm = _normalize_phone(phone)
        db = _load_alerts_db()
        reg = db.get("registrations", {}).get(norm, {})
        data = reg.get("portfolio", [])
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def _save_user_portfolio(phone: str, portfolio: list) -> None:
    """שומר את ה-Portfolio בחשבון הטלגרם של המשתמש"""
    try:
        norm = _normalize_phone(phone)
        db = _load_alerts_db()
        if norm in db.get("registrations", {}):
            db["registrations"][norm]["portfolio"] = portfolio
            _save_alerts_db(db)
    except Exception:
        pass


# ── Monte Carlo Price Simulation ──────────────────────────────────────────────
def run_monte_carlo(
    hist: "pd.DataFrame",
    current_price: float,
    n_sims: int = 1000,
    days_30: int = 30,
    days_365: int = 252,
) -> dict:
    """
    Geometric Brownian Motion simulation.
    Returns dict with Plotly figure + summary stats for 30d and 1y horizons.
    """
    if hist is None or hist.empty or current_price <= 0:
        return {}

    # Daily log-returns from last 252 trading days
    _close = hist["Close"].dropna().tail(252)
    if len(_close) < 20:
        return {}

    _log_ret = np.log(_close / _close.shift(1)).dropna()
    _mu  = float(_log_ret.mean())          # daily drift
    _sig = float(_log_ret.std())           # daily volatility

    if _sig == 0:
        return {}

    _rng = np.random.default_rng(seed=42)
    _max_days = days_365
    _dt = 1.0

    # Simulate all paths at once: shape (n_sims, max_days)
    _shocks = _rng.normal(
        (_mu - 0.5 * _sig ** 2) * _dt,
        _sig * np.sqrt(_dt),
        size=(n_sims, _max_days),
    )
    _cum = np.exp(np.cumsum(_shocks, axis=1))
    _paths = current_price * _cum  # shape (n_sims, max_days)

    def _stats(col_idx: int) -> dict:
        _vals = _paths[:, col_idx]
        return {
            "p10":    float(np.percentile(_vals, 10)),
            "p25":    float(np.percentile(_vals, 25)),
            "median": float(np.percentile(_vals, 50)),
            "p75":    float(np.percentile(_vals, 75)),
            "p90":    float(np.percentile(_vals, 90)),
            "mean":   float(_vals.mean()),
        }

    _s30  = _stats(min(days_30, _max_days) - 1)
    _s365 = _stats(_max_days - 1)

    # Build Plotly figure — fan chart with percentile bands
    _x = list(range(1, _max_days + 1))
    _p10  = [float(np.percentile(_paths[:, i], 10))  for i in range(_max_days)]
    _p25  = [float(np.percentile(_paths[:, i], 25))  for i in range(_max_days)]
    _p50  = [float(np.percentile(_paths[:, i], 50))  for i in range(_max_days)]
    _p75  = [float(np.percentile(_paths[:, i], 75))  for i in range(_max_days)]
    _p90  = [float(np.percentile(_paths[:, i], 90))  for i in range(_max_days)]

    _fig = go.Figure()

    # 80% confidence band (p10–p90)
    _fig.add_trace(go.Scatter(
        x=_x + _x[::-1],
        y=_p90 + _p10[::-1],
        fill="toself",
        fillcolor="rgba(99,102,241,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        name="80% Confidence",
        hoverinfo="skip",
    ))
    # 50% confidence band (p25–p75)
    _fig.add_trace(go.Scatter(
        x=_x + _x[::-1],
        y=_p75 + _p25[::-1],
        fill="toself",
        fillcolor="rgba(99,102,241,0.18)",
        line=dict(color="rgba(0,0,0,0)"),
        name="50% Confidence",
        hoverinfo="skip",
    ))
    # Median path
    _fig.add_trace(go.Scatter(
        x=_x, y=_p50,
        line=dict(color="#6366f1", width=2.5),
        name="Median Path",
    ))
    # Current price baseline
    _fig.add_hline(
        y=current_price,
        line_dash="dot",
        line_color="rgba(156,163,175,0.6)",
        annotation_text=f"Current ${current_price:.2f}",
        annotation_font_size=11,
    )
    # 30-day marker
    if days_30 <= _max_days:
        _fig.add_vline(
            x=days_30,
            line_dash="dash",
            line_color="rgba(250,204,21,0.5)",
            annotation_text="30d",
            annotation_font_size=10,
        )

    _fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=40, l=50, r=20),
        height=320,
        xaxis=dict(
            title="Trading Days",
            showgrid=False,
            color="#9ca3af",
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            title="Price ($)",
            showgrid=True,
            gridcolor="rgba(243,244,246,0.15)",
            color="#9ca3af",
            tickprefix="$",
            tickfont=dict(size=11),
        ),
        legend=dict(
            font=dict(size=11, color="#9ca3af"),
            bgcolor="rgba(0,0,0,0)",
            x=0, y=1,
        ),
        hovermode="x unified",
    )

    return {"fig": _fig, "s30": _s30, "s365": _s365, "vol_annual": _sig * np.sqrt(252)}


# ── Portfolio & Best Pick helpers ─────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def get_usd_ils() -> float:
    import time as _t
    for _a in range(3):
        try:
            rate = yf.Ticker("ILS=X").fast_info.get("lastPrice")
            if rate:
                return float(rate)
        except Exception as _e:
            if ("too many requests" in str(_e).lower() or "429" in str(_e)) and _a < 2:
                _t.sleep(2 * (2 ** _a))
                continue
        break
    # Fallback: try USDILS=X as alternative symbol
    try:
        rate2 = yf.Ticker("USDILS=X").fast_info.get("lastPrice")
        if rate2:
            return float(rate2)
    except Exception:
        pass
    return 3.7


@st.cache_data(ttl=180, show_spinner=False)
def fetch_portfolio_prices(tickers: tuple) -> dict:
    import time as _t

    def _fetch_one(t):
        for _a in range(3):
            try:
                fi = yf.Ticker(t).fast_info
                price = fi.get("lastPrice") or fi.get("previousClose") or 0
                if price:
                    return t, float(price)
            except Exception as _e:
                if ("too many requests" in str(_e).lower() or "429" in str(_e)) \
                        and _a < 2:
                    _t.sleep(2 * (2 ** _a))
                    continue
            break
        # Fallback: yf.download last close
        try:
            _dl = yf.download(t, period="2d", interval="1d",
                              auto_adjust=True, progress=False, threads=False)
            if _dl is not None and not _dl.empty:
                return t, float(_dl["Close"].iloc[-1])
        except Exception:
            pass
        return t, 0.0

    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(_fetch_one, tickers))
    return dict(results)


def portfolio_ai_analysis(holdings: list, usd_ils: float) -> str:
    if not holdings:
        return "התיק ריק."
    total_val = sum(h["value_usd"] for h in holdings)
    if total_val <= 0:
        return "לא ניתן לחשב ניתוח — ערך התיק הוא אפס."
    sector_vals: dict = {}
    for h in holdings:
        sec = h.get("sector", "Unknown")
        sector_vals[sec] = sector_vals.get(sec, 0) + h["value_usd"]
    top_sector = max(sector_vals, key=lambda k: sector_vals[k])
    top_pct = sector_vals[top_sector] / total_val * 100
    scores = [h.get("score", 50) for h in holdings]
    avg_score = sum(scores) / len(scores)
    low_score_stocks = [h["ticker"] for h in holdings if h.get("score", 50) < 40]
    total_ils = total_val * usd_ils
    lines = [
        f"**שווי תיק כולל:** ${total_val:,.0f} | ₪{total_ils:,.0f}",
        f"**ציון ממוצע:** {avg_score:.0f}/100",
    ]
    if top_pct > 50:
        lines.append(f"⚠️ **ריכוז גבוה בסקטור {top_sector}** ({top_pct:.0f}%) — שקול גיוון.")
    else:
        lines.append(f"✅ **פיזור סקטורי סביר** — {top_sector} מהווה {top_pct:.0f}% מהתיק.")
    if avg_score >= 70:
        lines.append("✅ **ציון ממוצע גבוה** — התיק מאוזן היטב.")
    elif avg_score >= 50:
        lines.append("⚠️ **ציון ממוצע בינוני** — ישנן הזדמנויות לשיפור.")
    else:
        lines.append("🔴 **ציון ממוצע נמוך** — כדאי לבחון מחדש את ההרכב.")
    if low_score_stocks:
        lines.append(f"🔴 **מניות עם ציון נמוך (<40):** {', '.join(low_score_stocks)} — שקול לבחון מחדש.")
    return "\n\n".join(lines)


# Crypto/mining tickers to exclude from best-pick scanner
_CRYPTO_MINING_EXCLUDE = {
    "RIOT","MARA","HUT","CLSK","BTBT","IREN","WULF","HIVE","CIFR","BITF",
    "CORZ","ARBK","DMGI","SDIG","GFAI","BSRT","GRIID","MIGI","NXGL","BTCS",
    "BFAR","CBIT","SLNH",
}

@st.cache_data(ttl=600, show_spinner=False)
def find_best_pick(horizon: str) -> list:
    """Scans all tickers and returns list of (ticker, score) sorted descending.
    Only includes stocks with sufficient fundamental data quality.
    """
    def _score_one(t):
        try:
            # Skip known crypto/mining tickers
            if t in _CRYPTO_MINING_EXCLUDE:
                return t, 0
            d = fetch_data(t)
            if d["hist"].empty or d.get("is_etf"):
                return t, 0
            # ── Data quality gates ────────────────────────────────────────
            # 1. Require meaningful market cap (≥ $1B)
            if d["mkt_cap"] < 1_000_000_000:
                return t, 0
            # 2. Price ≥ $1 (exclude penny stocks and unknown-price stocks)
            _cp = d.get("current_price", 0) or 0
            if _isnan(float(_cp)) or float(_cp) < 1.0:
                return t, 0
            # 3. Require ≥ 60 trading days of history
            if len(d["hist"]) < 60:
                return t, 0
            # 3b. Require average daily volume ≥ 100K (liquidity filter)
            _avg_vol = d["hist"]["Volume"].tail(30).mean() if "Volume" in d["hist"].columns else 0
            if _avg_vol < 100_000:
                return t, 0
            # 4. Must be actual equity, not crypto/commodity ETF
            if d.get("quote_type") not in ("EQUITY", None, ""):
                return t, 0
            # 5. Require at least ONE valid fundamental metric
            has_pe     = not _isnan(d["pe_ratio"]) and d["pe_ratio"] > 0
            has_cagr   = d["revenue_cagr"] > 0.01
            has_margin = not _isnan(d["gross_margins"]) and d["gross_margins"] > 0
            if not (has_pe or has_cagr or has_margin):
                return t, 0
            # ── Score ─────────────────────────────────────────────────────
            tech = compute_technicals(d["hist"])
            s = compute_score(d, tech, horizon, use_news=False)
            # 6. Scale penalty for missing fundamentals
            missing = sum([not has_pe, not has_cagr, not has_margin])
            if missing == 1:
                s = max(0, s - 5)    # 1 missing → -5 pts
            elif missing == 2:
                s = max(0, s - 15)   # 2 missing → -15 pts
            # 7. Penalize negative revenue CAGR stocks
            if d["revenue_cagr"] < -0.05:
                s = max(0, s - 8)
            return t, s
        except Exception:
            return t, 0
    with ThreadPoolExecutor(max_workers=50) as ex:
        results = list(ex.map(_score_one, TICKER_LIST))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# ── Candlestick + Indicators Chart ────────────────────────────────────────────
def build_chart(
    df: pd.DataFrame, tech: dict,
    ma1: int, ma2: int,
    selected_indicators: list[str]) -> go.Figure:
    subplot_inds = [i for i in SUBPLOT_INDS if i in selected_indicators]
    overlay_inds = [i for i in selected_indicators if i in OVERLAY_INDS]
    n_sub = len(subplot_inds)
    n_rows = 2 + n_sub

    # Dynamic row heights
    price_h  = max(280, 340 - n_sub * 15)
    volume_h = 70
    ind_h    = 120
    total_h  = price_h + volume_h + n_sub * ind_h
    row_heights = [price_h/total_h, volume_h/total_h] + [ind_h/total_h]*n_sub
    chart_height = min(1000, 540 + n_sub * 140)

    fig = make_subplots(
        rows=n_rows, cols=1, shared_xaxes=True,
        row_heights=row_heights, vertical_spacing=0.02)

    # ── Row 1: Candlestick ────────────────────────────────────────────────
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name="Price",
        increasing_line_color="#10b981", decreasing_line_color="#ef4444",
        increasing_fillcolor="#10b981", decreasing_fillcolor="#ef4444"), row=1, col=1)

    # ── Row 2: Volume ─────────────────────────────────────────────────────
    vol_colors = ["#10b981" if float(c) >= float(o) else "#ef4444"
                  for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"], marker_color=vol_colors,
        opacity=0.55, name="Volume", showlegend=False), row=2, col=1)

    # ── Price overlays ────────────────────────────────────────────────────
    if ma1 > 0:
        s1 = compute_ma_series(df, ma1)
        if not s1.empty:
            fig.add_trace(go.Scatter(
                x=df.index, y=s1.values, mode="lines",
                name=f"MA {ma1}", line=dict(color="#f59e0b", width=1.8)), row=1, col=1)

    if ma2 > 0 and ma2 != ma1:
        s2 = compute_ma_series(df, ma2)
        if not s2.empty:
            fig.add_trace(go.Scatter(
                x=df.index, y=s2.values, mode="lines",
                name=f"MA {ma2}", line=dict(color="#ef4444", width=1.8)), row=1, col=1)

    if "Bollinger Bands" in overlay_inds and not tech["bb_upper"].empty:
        fig.add_trace(go.Scatter(
            x=df.index, y=tech["bb_upper"].values, mode="lines",
            name="BB Upper", line=dict(color="rgba(99,102,241,.5)", width=1, dash="dash")), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=tech["bb_lower"].values, mode="lines",
            name="BB Lower", line=dict(color="rgba(99,102,241,.5)", width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(99,102,241,.06)"), row=1, col=1)

    if "VWAP" in overlay_inds and not tech["vwap"].empty:
        fig.add_trace(go.Scatter(
            x=df.index, y=tech["vwap"].values, mode="lines",
            name="VWAP", line=dict(color="#8b5cf6", width=1.5, dash="dot")), row=1, col=1)

    # ── Indicator subplots ────────────────────────────────────────────────
    for row_idx, ind in enumerate(subplot_inds, start=3):

        if ind == "RSI":
            rsi_s = tech["rsi_series"].dropna()
            if not rsi_s.empty:
                fig.add_trace(go.Scatter(
                    x=rsi_s.index, y=rsi_s.values,
                    name="RSI (14)", line=dict(color="#6366f1", width=1.5)), row=row_idx, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="#ef4444",
                          opacity=0.5, row=row_idx, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="#10b981",
                          opacity=0.5, row=row_idx, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color="rgba(0,0,0,0.15)",
                          row=row_idx, col=1)
            fig.update_yaxes(title_text="RSI", range=[0, 100],
                             row=row_idx, col=1,
                             title_font=dict(size=10), tickfont=dict(size=9))

        elif ind == "MACD":
            hist_s = tech["macd_hist_series"]
            macd_l = tech["macd_line"]
            sig_l  = tech["macd_signal"]
            if not hist_s.empty:
                hcolors = ["#10b981" if v >= 0 else "#ef4444"
                           for v in hist_s.fillna(0)]
                fig.add_trace(go.Bar(
                    x=df.index, y=hist_s.values,
                    marker_color=hcolors, opacity=0.7,
                    name="MACD Hist", showlegend=True), row=row_idx, col=1)
            if not macd_l.empty:
                fig.add_trace(go.Scatter(
                    x=df.index, y=macd_l.values,
                    name="MACD", line=dict(color="#6366f1", width=1.2)), row=row_idx, col=1)
            if not sig_l.empty:
                fig.add_trace(go.Scatter(
                    x=df.index, y=sig_l.values,
                    name="Signal", line=dict(color="#f59e0b", width=1.2)), row=row_idx, col=1)
            fig.add_hline(y=0, line_color="rgba(0,0,0,0.2)",
                          row=row_idx, col=1)
            fig.update_yaxes(title_text="MACD", row=row_idx, col=1,
                             title_font=dict(size=10), tickfont=dict(size=9))

        elif ind == "Stochastic":
            sk, sd = tech["stoch_k"], tech["stoch_d"]
            if not sk.empty:
                fig.add_trace(go.Scatter(
                    x=df.index, y=sk.values,
                    name="%K", line=dict(color="#6366f1", width=1.2)), row=row_idx, col=1)
            if not sd.empty:
                fig.add_trace(go.Scatter(
                    x=df.index, y=sd.values,
                    name="%D", line=dict(color="#f59e0b", width=1.2, dash="dot")), row=row_idx, col=1)
            fig.add_hline(y=80, line_dash="dash", line_color="#ef4444",
                          opacity=0.5, row=row_idx, col=1)
            fig.add_hline(y=20, line_dash="dash", line_color="#10b981",
                          opacity=0.5, row=row_idx, col=1)
            fig.update_yaxes(title_text="Stoch", range=[0, 100],
                             row=row_idx, col=1,
                             title_font=dict(size=10), tickfont=dict(size=9))

        elif ind == "OBV":
            obv_s = tech["obv"]
            if not obv_s.empty:
                fig.add_trace(go.Scatter(
                    x=df.index, y=obv_s.values,
                    name="OBV", line=dict(color="#6366f1", width=1.2),
                    fill="tozeroy", fillcolor="rgba(99,102,241,0.07)"), row=row_idx, col=1)
            fig.update_yaxes(title_text="OBV", row=row_idx, col=1,
                             title_font=dict(size=10), tickfont=dict(size=9))

        elif ind == "ATR":
            atr_s = tech["atr"]
            if not atr_s.empty:
                fig.add_trace(go.Scatter(
                    x=df.index, y=atr_s.values,
                    name="ATR (14)", line=dict(color="#f97316", width=1.5)), row=row_idx, col=1)
            fig.update_yaxes(title_text="ATR", row=row_idx, col=1,
                             title_font=dict(size=10), tickfont=dict(size=9))

    # ── Global layout ─────────────────────────────────────────────────────
    spike = dict(showspikes=True, spikemode="across", spikesnap="cursor",
                 spikecolor="#6366f1", spikethickness=1, spikedash="solid")
    fig.update_layout(
        height=chart_height,
        paper_bgcolor="#fcfcfc", plot_bgcolor="#fcfcfc",
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.01,
                    xanchor="left", x=0, font=dict(size=10)),
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
        xaxis=dict(**spike, gridcolor="rgba(0,0,0,.04)"),
        yaxis=dict(**spike, gridcolor="rgba(0,0,0,.04)"),
        xaxis2=dict(**spike),
        yaxis2=dict(gridcolor="rgba(0,0,0,.04)"),
        font=dict(family="Inter, sans-serif", size=11))
    # Apply gridcolor to all indicator axes
    for i in range(3, n_rows+1):
        fig.update_xaxes(dict(**spike), row=i, col=1)
        fig.update_yaxes(gridcolor="rgba(0,0,0,.04)", row=i, col=1)

    fig.update_traces(xaxis="x1")
    return fig



# ── Financial term tooltip helper ─────────────────────────────────────────────
_GLOSSARY: dict[str, str] = {
    "RSI": "Relative Strength Index (14 days) — momentum oscillator 0-100. "
           "Above 70 = overbought (may pull back). Below 30 = oversold (may bounce). "
           "50 is neutral.",
    "MACD": "Moving Average Convergence Divergence — difference between 12-day "
            "and 26-day exponential moving averages. Positive histogram = bullish "
            "momentum; negative = bearish pressure.",
    "P/E": "Price-to-Earnings ratio — how many dollars investors pay per $1 of "
           "annual earnings. Lower = cheaper. Typical market average ~20x. "
           "High-growth stocks often trade 40-100x.",
    "PEG": "Price/Earnings-to-Growth — P/E divided by annual earnings growth rate. "
           "PEG < 1 = potentially undervalued relative to growth. "
           "PEG > 2 = growth priced in or expensive.",
    "CAGR": "Compound Annual Growth Rate — the smoothed annual rate at which "
            "revenue grew over multiple years. Formula: (End/Start)^(1/years) - 1.",
    "FCF Yield": "Free Cash Flow Yield — free cash flow divided by market cap. "
                 "Higher = more cash generated per dollar invested. "
                 ">4% is generally considered healthy.",
    "Gross Margin": "Gross Profit ÷ Revenue. Measures how much revenue remains "
                    "after direct production costs. >40% indicates pricing power "
                    "and a competitive moat.",
    "Market Cap": "Total market value of all outstanding shares "
                  "(Price × Shares Outstanding). Mega-cap: >$200B. "
                  "Large-cap: $10B-$200B. Mid-cap: $2B-$10B.",
    "MA 50": "50-Day Moving Average — average closing price over the last 50 "
             "trading days. A key short-term trend indicator. Price above MA50 "
             "= short-term bullish.",
    "MA 150": "150-Day Moving Average — medium-term trend. Often used by "
              "institutional investors for swing and positional trades.",
    "EPS": "Earnings Per Share — net profit divided by number of shares. "
           "Higher EPS over time signals consistent profitability.",
    "Forward P/E": "P/E calculated using next 12 months estimated earnings "
                   "instead of trailing. Lower Forward P/E vs Trailing = "
                   "earnings expected to grow.",
    "VWAP": "Volume Weighted Average Price — average price weighted by volume "
            "traded throughout the period. Institutional traders use it as "
            "a benchmark for trade execution quality.",
    "ATR": "Average True Range (14 days) — measures daily price volatility. "
           "Higher ATR = more volatile stock = wider stop-losses needed.",
    "OBV": "On-Balance Volume — cumulative volume indicator. Rising OBV on "
           "flat price = accumulation (bullish). Falling OBV = distribution.",
    "Stochastic": "Stochastic Oscillator — compares closing price to price "
                  "range over 14 days. %K above 80 = overbought; below 20 = oversold.",
    "Bollinger Bands": "Volatility bands set 2 standard deviations above/below "
                       "a 20-day moving average. Price touching upper band = "
                       "overbought; lower band = potential support.",
}

def _term(label: str, key: str | None = None) -> str:
    """Wrap a financial term in a hover-tooltip span."""
    defn = _GLOSSARY.get(key or label, "")
    if not defn:
        return label
    safe = defn.replace('"', '&quot;')
    return f'<span class="term" data-def="{safe}">{label}</span>'

# ── Executive Report ──────────────────────────────────────────────────────────
def _badge(text: str, kind: str) -> str:
    return f'<span class="badge badge-{kind}">{text}</span>'

def _row(name: str, value: str, blabel: str, bkind: str) -> str:
    return (f'<div class="rpt-row">'
            f'<span class="rpt-name">{name}</span>'
            f'<span style="display:flex;gap:12px;align-items:center;">'
            f'<span class="rpt-value">{value}</span>'
            f'{_badge(blabel, bkind)}</span></div>')

def build_report(ticker: str, data: dict, tech: dict, score: int, horizon: str) -> str:
    cname   = data["company_name"]
    price   = data["current_price"]
    pe      = data["pe_ratio"]
    fpe     = data["forward_pe"]
    peg     = data["peg_ratio"]
    margins = data["gross_margins"]
    cagr    = data["revenue_cagr"]
    fcfy    = data["fcf_yield"]
    sector  = data["sector"]
    mktcap  = data["mkt_cap"]
    rsi     = tech["rsi"]
    macd    = tech["macd_hist"]

    # Horizon-aware MA reference
    is_short = (horizon == "30D Tactical")
    ma_period = 50 if is_short else 150
    ma_val    = tech["ma50"] if is_short else tech["ma150"]
    ma_label  = f"MA {ma_period}"

    # Verdict
    if score >= 80:   verdict, vcolor = "STRONG BUY", "#059669"
    elif score >= 65: verdict, vcolor = "BUY",         "#d97706"
    elif score >= 45: verdict, vcolor = "HOLD",        "#c2410c"
    else:             verdict, vcolor = "SELL",        "#dc2626"
    confidence = min(95, 50 + abs(score - 50))

    # CEO summary
    m_txt  = fmt_pct(float(margins)) if not _isnan(float(margins)) else "N/A"
    p_txt  = f"{float(peg):.2f}"     if not _isnan(float(peg))     else "N/A"
    c_txt  = fmt_pct(float(cagr))    if float(cagr) != 0           else "N/A"
    cap_txt = fmt_mcap(mktcap) if mktcap > 0 else "N/A"

    s1 = (f"{cname} ({ticker}) is a {sector} company with a Sovereign Score of {score}/100 "
          f"under the {horizon} framework, reflecting "
          f"{'exceptional' if score>=75 else 'solid' if score>=55 else 'moderate'} positioning.")
    s2 = (f"Gross margins of {m_txt} "
          f"{'demonstrate a high-moat advantage' if not _isnan(float(margins)) and float(margins)>0.40 else 'reflect industry-standard efficiency'}, "
          f"with revenue CAGR of {c_txt} signaling "
          f"{'robust' if float(cagr)>0.15 else 'measured'} growth.")
    if is_short:
        s3_prefix = f"RSI-14 of {round(rsi, 1)} and "
    else:
        fpe_str = f"{float(fpe):.1f}x" if not _isnan(float(fpe)) else "N/A"
        pe_str2 = f"{float(pe):.1f}x"  if not _isnan(float(pe))  else "N/A"
        s3_prefix = f"Forward P/E of {fpe_str} vs trailing {pe_str2}, "
    s3 = f"{s3_prefix}PEG of {p_txt}: the risk/reward warrants a {verdict} stance with {confidence}% confidence."

    # Fundamental rows
    def fb(v, lo, hi):
        if _isnan(v): return "N/A", "gray"
        return ("Strong","green") if v>=hi else ("Moderate","yellow") if v>=lo else ("Weak","red")

    mar_lbl = ("High-Moat","green") if not _isnan(float(margins)) and float(margins)>0.40 else \
              ("Average","yellow") if not _isnan(float(margins)) and float(margins)>0.20 else ("Thin","red")
    cap_lbl = ("Mega-Cap","blue") if mktcap>MEGA_CAP_THRESHOLD else ("Large-Cap","gray")
    fund_rows = (
        _row(_term("Revenue CAGR","CAGR"),  c_txt,  *fb(float(cagr), 0.05, 0.15)) +
        _row(_term("Gross Margins","Gross Margin"), m_txt,  *mar_lbl) +
        _row(_term("FCF Yield","FCF Yield"),     fmt_pct(float(fcfy)) if not _isnan(float(fcfy)) else "N/A",
             *fb(float(fcfy) if not _isnan(float(fcfy)) else float("nan"), 0.02, 0.04)) +
        _row(_term("Market Cap","Market Cap"),    cap_txt, *cap_lbl)
    )

    # Valuation rows
    pe_lbl  = "Fair" if not _isnan(float(pe)) and float(pe)<30 else "Elevated"
    pe_clr  = "green" if pe_lbl=="Fair" else "yellow"
    peg_lbl = "Attractive" if not _isnan(float(peg)) and float(peg)<1.5 else "Fair Value" if not _isnan(float(peg)) and float(peg)<2.5 else "Rich"
    peg_clr = "green" if peg_lbl=="Attractive" else "yellow" if peg_lbl=="Fair Value" else "red"

    val_rows = (
        _row(_term("Trailing P/E","P/E"),  f"{float(pe):.1f}x"  if not _isnan(float(pe))  else "N/A", pe_lbl,  pe_clr) +
        _row(_term("Forward P/E","Forward P/E"),   f"{float(fpe):.1f}x" if not _isnan(float(fpe)) else "N/A",
             "Discount to TTM" if not _isnan(float(fpe)) and not _isnan(float(pe)) and float(fpe)<float(pe) else "N/A", "gray") +
        _row(_term("PEG Ratio","PEG"),      p_txt,               peg_lbl, peg_clr)
    )

    # Technical rows — HORIZON AWARE
    rsi_lbl = ("Overbought" if float(rsi)>70 else "Oversold" if float(rsi)<30
               else "Neutral" if 40<=float(rsi)<=60 else f"{'Bullish' if float(rsi)>50 else 'Bearish'}")
    rsi_clr = "red" if float(rsi)>70 else "yellow" if float(rsi)<30 else "green"
    macd_lbl = "Bullish Momentum" if float(macd)>0 else "Bearish Pressure"
    macd_clr = "green" if float(macd)>0 else "red"
    ma_above = not _isnan(float(ma_val)) and float(price) > float(ma_val)
    ma_pos  = f"Above {ma_label}" if ma_above else f"Below {ma_label}"
    ma_clr  = "green" if ma_above else "red"
    if not _isnan(float(ma_val)) and float(ma_val)>0 and not _isnan(float(price)):
        ma_diff = (float(price)-float(ma_val))/float(ma_val)*100
        ma_val_str = f"{fmt_price(float(price))}  ({'+' if ma_diff>=0 else ''}{ma_diff:.1f}%)"
    else:
        ma_val_str = "N/A"

    # Short-term shows RSI + MACD + MA50; Long-term shows MA150 + forward PE note
    if is_short:
        tech_rows = (
            _row(_term("RSI-14","RSI"),          f"{float(rsi):.1f}",   rsi_lbl,  rsi_clr) +
            _row(_term("MACD Histogram","MACD"),  f"{float(macd):+.4f}", macd_lbl, macd_clr) +
            _row(_term(f"vs. {ma_label}", "MA 50" if is_short else "MA 150"), ma_val_str,             ma_pos,   ma_clr)
        )
        tech_note = "Short-term technicals: RSI momentum, MACD trend, and 50-day moving average are primary signals."
    else:
        vol_52w = ""
        tech_rows = (
            _row(_term(f"vs. {ma_label}", "MA 50" if is_short else "MA 150"), ma_val_str,             ma_pos,   ma_clr) +
            _row("RSI-14",          f"{float(rsi):.1f}",   rsi_lbl,  rsi_clr) +
            _row("MACD Histogram",  f"{float(macd):+.4f}", macd_lbl, macd_clr)
        )
        tech_note = "Long-term technicals: 150-day trend provides strategic positioning context, complementing fundamental analysis."

    # Bullish arguments
    bulls = []
    if not _isnan(float(margins)) and float(margins)>0.35:
        bulls.append(("🏰","High-Margin Moat", f"Gross margins of {m_txt} indicate durable pricing power and competitive advantage."))
    if not _isnan(float(peg)) and 0<float(peg)<1.5:
        bulls.append(("📐","GARP Opportunity", f"PEG of {p_txt} suggests the market underprices the growth runway."))
    if float(cagr)>0.10:
        bulls.append(("📈","Revenue Momentum", f"CAGR of {c_txt} shows consistent top-line expansion."))
    if not _isnan(float(fcfy)) and float(fcfy)>0.03:
        bulls.append(("💸","FCF Generation", f"FCF yield of {fmt_pct(float(fcfy))} funds buybacks and strategic M&A."))
    if mktcap>MEGA_CAP_THRESHOLD:
        bulls.append(("🏦","Mega-Cap Stability", f"{cap_txt} ensures index inclusion and institutional buying flows."))
    if float(rsi)<45 and float(rsi)>25:
        bulls.append(("🔁","Tactical Entry", f"RSI of {rsi:.1f} suggests potential mean-reversion opportunity."))
    generic = [
        ("🌐","Sector Leadership", f"As a {sector} leader, {ticker} benefits from brand scale and distribution moats."),
        ("📊","Passive Demand", "Mega-cap status ensures persistent buying from index-tracking vehicles."),
        ("🔬","Innovation Pipeline", "Sustained R&D investment positions the company for next-cycle leadership.")]
    i = 0
    while len(bulls)<3:
        bulls.append(generic[i%len(generic)]); i+=1
    bulls = bulls[:3]

    bulls_html = "".join(
        f'<li class="thesis-item"><span class="thesis-icon">{ic}</span>'
        f'<span><span class="thesis-title">{t}</span> — {d}</span></li>'
        for ic,t,d in bulls
    )

    pe_str = f"{float(pe):.1f}x" if not _isnan(float(pe)) else "current"
    risks = [
        ("⚠️","Rate Sensitivity", f"Multiple compression risk: {pe_str} P/E leaves limited cushion if earnings disappoint in a high-rate environment."),
        ("⚙️","Execution Risk", f"Sustaining {c_txt} growth in a maturing market requires disciplined capital allocation.")]
    risks_html = "".join(
        f'<li class="thesis-item"><span class="thesis-icon">{ic}</span>'
        f'<span><span class="thesis-title">{t}</span> — {d}</span></li>'
        for ic,t,d in risks
    )

    return f"""
<div class="exec-card">
  <div class="ceo-summary">
    <div class="ceo-summary-title">&#9650; CEO Executive Summary</div>
    <p>{s1}</p><p>{s2}</p><p>{s3}</p>
  </div>
  <div class="report-section">
    <div class="report-section-title">1 — Fundamental Health</div>{fund_rows}
  </div>
  <div class="report-section">
    <div class="report-section-title">2 — Valuation Analysis</div>{val_rows}
  </div>
  <div class="report-section">
    <div class="report-section-title">3 — Technical Positioning
      <span style="font-size:11px;font-weight:400;color:#9ca3af;margin-left:8px;">{tech_note}</span>
    </div>{tech_rows}
  </div>
  <div class="report-section">
    <div class="report-section-title">4 — Catalysts &amp; Growth Drivers</div>
    <ul class="thesis-list">{bulls_html}</ul>
  </div>
  <div class="report-section">
    <div class="report-section-title">5 — Strategic Risk Assessment</div>
    <ul class="thesis-list">{risks_html}</ul>
  </div>
  <div class="verdict-box">
    <span class="verdict-label" style="color:{vcolor};">{verdict}</span>
    <div class="verdict-meta">Confidence: {confidence}%<br>Sovereign Score: {score} / 100<br>Horizon: {horizon}</div>
  </div>
</div>"""


# ── Peer Comparison (includes self) ───────────────────────────────────────────
def get_peers_for(ticker: str) -> list[str]:
    """Find up to 5 peers from the same sector group."""
    t = ticker.upper()
    # Search all sector groups for this ticker
    best: list[str] = []
    for group in SECTOR_GROUPS.values():
        if t in group:
            candidates = [s for s in group if s != t]
            if len(candidates) > len(best):
                best = candidates  # pick the most specific group
    return best[:5]


@st.cache_data(ttl=300, show_spinner=False)
def build_peers(ticker: str, self_data: dict | None = None, extra_peers: tuple = ()) -> pd.DataFrame:
    peers = get_peers_for(ticker)
    # Merge extra_peers without duplicates
    all_peers = list(dict.fromkeys(peers + [p for p in extra_peers if p != ticker.upper()]))
    if not all_peers:
        return pd.DataFrame()

    # Use fetch_data (with all fallbacks) for every peer
    def _one(sym: str) -> tuple[str, dict]:
        try:
            return sym, fetch_data(sym)
        except Exception:
            return sym, {}

    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(_one, all_peers))

    def _row_from(sym: str, d: dict, is_self: bool = False) -> dict:
        mc = float(_safe(d.get("mkt_cap", 0.0), 0.0))
        p  = float(_safe(d.get("current_price", float("nan")), float("nan")))
        pe = float(_safe(d.get("pe_ratio",  float("nan")), float("nan")))
        pg = float(_safe(d.get("peg_ratio", float("nan")), float("nan")))
        gm = float(_safe(d.get("gross_margins", float("nan")), float("nan")))
        label = f"★ {sym}" if is_self else sym
        return {
            "Ticker":       label,
            "Price":        fmt_price(p),
            "P/E":          f"{pe:.1f}x" if not _isnan(pe) else "N/A",
            "PEG":          f"{pg:.2f}"  if not _isnan(pg) else "N/A",
            "Market Cap":   fmt_mcap(mc) if mc > 0 else "N/A",
            "Gross Margin": fmt_pct(gm)  if not _isnan(gm) else "N/A",
        }

    rows = []
    # Add self first — uses the already-loaded fetch_data result from main flow
    if self_data:
        rows.append(_row_from(ticker.upper(), self_data, is_self=True))
    # Add peers
    for sym, d in results:
        rows.append(_row_from(sym, d))

    return pd.DataFrame(rows)


# ── Metric Cards ──────────────────────────────────────────────────────────────
def render_metric_cards(data: dict, tech: dict) -> None:
    price = data["current_price"]; prev = data["prev_close"]
    pct = ((float(price)-float(prev))/float(prev)*100) if (not _isnan(price) and not _isnan(prev) and float(prev)!=0) else float("nan")
    pct_cls  = "positive" if not _isnan(pct) and pct>=0 else "negative"
    pct_sign = "+" if not _isnan(pct) and pct>=0 else ""
    pe  = data["pe_ratio"]; peg = data["peg_ratio"]; mc = data["mkt_cap"]
    w52h = data.get("week52_high", float("nan"))
    w52l = data.get("week52_low",  float("nan"))
    peg_sub_cls = ("positive" if not _isnan(float(peg)) and float(peg)<1.5
                   else "negative" if not _isnan(float(peg)) and float(peg)>2.5 else "neutral")
    peg_sub = ("Attractive" if not _isnan(float(peg)) and float(peg)<1.5
               else "Rich" if not _isnan(float(peg)) and float(peg)>2.5
               else "Fair Value" if not _isnan(float(peg)) else "N/A")
    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-card">
        <div class="metric-label">Price</div>
        <div class="metric-value">{fmt_price(float(price)) if not _isnan(float(price)) else "N/A"}</div>
        <div class="metric-sub {pct_cls}">{f'{pct_sign}{pct:.2f}%' if not _isnan(pct) else 'N/A'}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">52-Week Range</div>
        <div class="metric-value" style="font-size:15px;">{fmt_price(float(w52h)) if not _isnan(float(w52h)) else "N/A"}</div>
        <div class="metric-sub neutral">Low: {fmt_price(float(w52l)) if not _isnan(float(w52l)) else "N/A"}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">P/E Ratio</div>
        <div class="metric-value">{f"{float(pe):.1f}x" if not _isnan(float(pe)) else "N/A"}</div>
        <div class="metric-sub neutral">Trailing Twelve Months</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Market Cap</div>
        <div class="metric-value">{fmt_mcap(mc) if mc>0 else "N/A"}</div>
        <div class="metric-sub neutral">{'Mega-Cap' if mc>MEGA_CAP_THRESHOLD else 'Large-Cap' if mc>10e9 else 'Mid-Cap'}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">PEG Ratio</div>
        <div class="metric-value">{f"{float(peg):.2f}" if not _isnan(float(peg)) else "N/A"}</div>
        <div class="metric-sub {peg_sub_cls}">{peg_sub}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Analyst Card ──────────────────────────────────────────────────────────────
def render_analyst_card(data: dict) -> None:
    n     = data["n_analysts"]
    rmean = data["rec_mean"]
    t_low = data["analyst_target_low"]
    t_mean= data["analyst_target_mean"]
    t_high= data["analyst_target_high"]
    price = data["current_price"]

    if n == 0 and _isnan(t_mean):
        return

    if not _isnan(rmean):
        if   float(rmean)<=1.5: rc,rl = "#10b981","STRONG BUY"
        elif float(rmean)<=2.5: rc,rl = "#34d399","BUY"
        elif float(rmean)<=3.5: rc,rl = "#f59e0b","HOLD"
        elif float(rmean)<=4.5: rc,rl = "#f97316","UNDERPERFORM"
        else:                   rc,rl = "#ef4444","SELL"
    else:
        rc,rl = "#6b7280", data["rec_key"].upper().replace("_"," ")

    upside_html = ""
    if not _isnan(t_mean) and not _isnan(price) and float(price)>0:
        upside = (float(t_mean)-float(price))/float(price)*100
        uc = "#10b981" if upside>=0 else "#ef4444"
        upside_html = (f'<span style="color:{uc};font-weight:700;'
                       f'font-family:\'JetBrains Mono\',monospace;">'
                       f'{"+" if upside>=0 else ""}{upside:.1f}%</span> upside to mean target')

    bar_pct = 50
    if not _isnan(t_low) and not _isnan(t_high) and float(t_high)>float(t_low) and not _isnan(t_mean):
        bar_pct = max(5, min(95, int((float(t_mean)-float(t_low))/(float(t_high)-float(t_low))*100)))

    hx = rc.lstrip("#")
    rec_bg = f"rgba({int(hx[0:2],16)},{int(hx[2:4],16)},{int(hx[4:6],16)},0.12)"
    mean_txt = f"{float(rmean):.2f}/5.00" if not _isnan(rmean) else "N/A"

    st.markdown(f"""
    <div class="analyst-card">
      <div class="analyst-block">
        <div class="analyst-lbl">Wall St. Consensus</div>
        <div><span class="rec-badge" style="background:{rec_bg};color:{rc};">{rl}</span></div>
        <div class="analyst-sub" style="margin-top:4px;">{n} analysts &nbsp;·&nbsp; Mean {mean_txt}</div>
      </div>
      <div class="analyst-block" style="flex:1;min-width:240px;">
        <div class="analyst-lbl">12-Month Price Targets</div>
        <div class="price-bar-track"><div class="price-bar-fill" style="width:{bar_pct}%;"></div></div>
        <div class="price-bar-labels">
          <span>Low {fmt_price(float(t_low)) if not _isnan(t_low) else "N/A"}</span>
          <span>Mean {fmt_price(float(t_mean)) if not _isnan(t_mean) else "N/A"}</span>
          <span>High {fmt_price(float(t_high)) if not _isnan(t_high) else "N/A"}</span>
        </div>
      </div>
      <div class="analyst-block">
        <div class="analyst-lbl">Implied Move</div>
        <div class="analyst-val">{fmt_price(float(t_mean)) if not _isnan(t_mean) else "N/A"}</div>
        <div class="analyst-sub">{upside_html}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def score_badge_html(score: int, is_etf: bool = False) -> str:
    if is_etf:
        return ('<span class="score-badge" style="background:rgba(99,102,241,.1);'
                'color:#6366f1;border:1px solid rgba(99,102,241,.3);">'
                '&#9673; ETF / FUND</span>')
    if score>=80:   bg,c,l = "rgba(16,185,129,.12)","#10b981","STRONG BUY"
    elif score>=65: bg,c,l = "rgba(245,158,11,.12)", "#f59e0b","BUY"
    elif score>=45: bg,c,l = "rgba(249,115,22,.12)", "#f97316","HOLD"
    else:           bg,c,l = "rgba(239,68,68,.12)",  "#ef4444","SELL"
    return (f'<span class="score-badge" style="background:{bg};color:{c};border:1px solid {c}40;">'
            f'&#9889; {score} &middot; {l}</span>')

EDEN_LOGO = """
<div class="eden-logo">
  <div class="eden-icon">E</div>
  <div><div class="eden-brand">Eden Sovereign</div>
       <div class="eden-sub">Intelligence Terminal</div></div>
</div>"""



# ── Financial value formatter ──────────────────────────────────────────────────
def fmt_fin_val(v) -> str:
    try:
        f = float(v)
        if f != f: return "N/A"
        if abs(f) >= 1e9: return f"${f/1e9:.2f}B"
        if abs(f) >= 1e6: return f"${f/1e6:.1f}M"
        return f"${f:,.0f}"
    except:
        return "N/A"


# ── News Tab ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def build_news(ticker: str) -> None:
    try:
        articles = yf.Ticker(ticker).news or []
    except Exception:
        articles = []
    if not articles:
        st.info("No recent news found for this ticker.")
        return

    import time as _time
    now = _time.time()

    def _parse_article(a: dict) -> tuple[str, str, str, float]:
        """Return (title, link, publisher, unix_ts). Handles old & new yfinance."""
        # New yfinance wraps fields under 'content'
        content = a.get("content") or {}
        title = (a.get("title") or content.get("title") or
                 content.get("clickThroughUrl", {}).get("url") or "")
        link  = (a.get("link") or
                 content.get("canonicalUrl", {}).get("url") or
                 content.get("clickThroughUrl", {}).get("url") or "#")
        pub   = (a.get("publisher") or
                 content.get("provider", {}).get("displayName") or "")
        ts    = a.get("providerPublishTime") or 0
        if not ts or ts == 0:
            # Try pubDate string: "2026-03-07T10:00:00Z"
            pub_date = content.get("pubDate") or a.get("pubDate") or ""
            if pub_date:
                try:
                    dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                    ts = dt.timestamp()
                except Exception:
                    ts = 0
        return title, link, pub, float(ts)

    cards = []
    for a in articles[:15]:
        title, link, pub, ts = _parse_article(a)
        if not title:
            continue
        diff = int(now - ts) if ts > 0 else -1
        if diff < 0:
            tago = ""
        elif diff < 3600:
            tago = f"{max(1, diff//60)} min ago"
        elif diff < 86400:
            tago = f"{diff//3600} hr ago"
        else:
            tago = f"{diff//86400} days ago"
        meta = " &nbsp;&middot;&nbsp; ".join(filter(None, [pub, tago]))
        cards.append(
            f'<div class="news-card">'
            f'<div class="news-title"><a href="{link}" target="_blank">{title}</a></div>'
            f'<div class="news-meta">{meta}</div>'
            f'</div>'
        )
    if not cards:
        st.info("No recent news found for this ticker.")
        return
    st.markdown('<div>' + "".join(cards) + '</div>', unsafe_allow_html=True)


# ── Financials Tab ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_financials(ticker: str) -> tuple:
    import time as _t
    obj = yf.Ticker(ticker)

    def _get(attr_primary: str, attr_fallback: str | None = None):
        for _attempt in range(3):
            try:
                val = getattr(obj, attr_primary, None)
                if val is not None and not (hasattr(val, "empty") and val.empty):
                    return val
                if attr_fallback:
                    val2 = getattr(obj, attr_fallback, None)
                    if val2 is not None and not (hasattr(val2, "empty") and val2.empty):
                        return val2
                return val
            except Exception as _e:
                _msg = str(_e).lower()
                if ("too many requests" in _msg or "429" in _msg or "rate limit" in _msg) \
                        and _attempt < 2:
                    _t.sleep(3 * (2 ** _attempt))
                    continue
                return None
        return None

    inc = _get("financials", "income_stmt")
    bal = _get("balance_sheet")
    cf  = _get("cashflow", "cash_flow")
    return inc, bal, cf


def build_financials(ticker: str) -> None:
    with st.spinner("Loading financial statements..."):
        inc, bal, cf = _fetch_financials(ticker)
    choice = st.radio("", ["Income Statement", "Balance Sheet", "Cash Flow"],
                      horizontal=True, label_visibility="collapsed")
    df_raw = {"Income Statement": inc, "Balance Sheet": bal, "Cash Flow": cf}[choice]
    if df_raw is None or df_raw.empty:
        st.info("Financial statements not available.")
        return
    df_t = df_raw.T.copy()
    df_t.index = [str(i)[:10] for i in df_t.index]
    # Reorder: show important rows first
    PRIORITY = [
        "Total Revenue", "Revenue",
        "Gross Profit",
        "Operating Income", "EBIT",
        "EBITDA", "Normalized EBITDA",
        "Net Income", "Net Income Common Stockholders",
        "Basic EPS", "Diluted EPS",
        "Operating Cash Flow", "Free Cash Flow", "Capital Expenditure",
        "Total Assets", "Total Debt", "Cash And Cash Equivalents",
        "Stockholders Equity", "Total Liabilities Net Minority Interest",
    ]
    cols = list(df_t.columns)
    ordered = [c for c in PRIORITY if c in cols] + [c for c in cols if c not in PRIORITY]
    df_t = df_t[ordered]
    df_fmt = df_t.map(fmt_fin_val)
    st.dataframe(df_fmt, use_container_width=True)


# ── Earnings Tab ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_earnings(ticker: str):
    obj = yf.Ticker(ticker)
    # Try get_earnings_dates (requires lxml, installed)
    try:
        df = obj.get_earnings_dates(limit=12)
        if df is not None and not df.empty:
            return df
    except Exception:
        pass
    # Fallback: earnings_history (no lxml needed, decimal surprise)
    try:
        df = obj.earnings_history
        if df is not None and not df.empty:
            # Normalise column names to match get_earnings_dates format
            df = df.rename(columns={
                "epsActual":       "Reported EPS",
                "epsEstimate":     "EPS Estimate",
                "surprisePercent": "Surprise(%)",
            })
            if "Surprise(%)" in df.columns:
                df["Surprise(%)"] = df["Surprise(%)"] * 100  # decimal → %
            df.index.name = "Earnings Date"
            return df
    except Exception:
        pass
    return None


def build_earnings(ticker: str, info: dict) -> None:
    with st.spinner("Loading earnings data..."):
        df_all = _fetch_earnings(ticker)

    if df_all is None or df_all.empty:
        st.info("Earnings data not available.")
        return

    # Separate future (no Reported EPS) from history
    rep_col = "Reported EPS"
    future_rows = df_all[df_all[rep_col].isna()] if rep_col in df_all.columns else df_all.iloc[:0]
    past_rows   = df_all[df_all[rep_col].notna()] if rep_col in df_all.columns else df_all

    # Next earnings banner — from df (most reliable source)
    if not future_rows.empty:
        next_idx = future_rows.index[0]
        try:
            next_dt   = pd.Timestamp(next_idx).tz_localize(None) if pd.Timestamp(next_idx).tzinfo else pd.Timestamp(next_idx)
            days_away = (next_dt - pd.Timestamp(datetime.now())).days
            est       = future_rows.iloc[0].get("EPS Estimate")
            est_str   = f"  &nbsp;·&nbsp; EPS est. ${float(est):.2f}" if est and not pd.isna(est) else ""
            st.markdown(
                f'<div class="earn-next">&#128197; Next Earnings: '
                f'<strong>{next_dt.strftime("%b %d, %Y")}</strong>'
                f' &nbsp;&mdash;&nbsp; {max(0, days_away)} days away{est_str}</div>',
                unsafe_allow_html=True,
            )
        except Exception:
            pass

    if past_rows.empty:
        st.info("No historical earnings data.")
        return

    def _surp_html(v):
        try:
            f = float(v)
            color = "#10b981" if f >= 0 else "#ef4444"
            sign  = "+" if f >= 0 else ""
            return f'<span style="color:{color};font-weight:600">{sign}{f:.2f}%</span>'
        except:
            return "N/A"

    rows_html = ""
    for idx, row in past_rows.head(10).iterrows():
        date_str = str(idx)[:10]
        def _cell(col):
            v = row.get(col)
            if v is None or (hasattr(v, '__class__') and v.__class__.__name__ == 'float' and v != v):
                return "N/A"
            try: return f"${float(v):.2f}"
            except: return str(v)
        eps_est  = _cell("EPS Estimate")
        eps_rep  = _cell("Reported EPS")
        surp     = _surp_html(row.get("Surprise(%)"))
        td  = 'style="padding:9px 12px;font-family:\'JetBrains Mono\',monospace;font-size:12px;border-bottom:1px solid #f3f4f6"'
        tdc = f'style="padding:9px 12px;font-size:12px;border-bottom:1px solid #f3f4f6"'
        rows_html += (f"<tr>"
                      f"<td {td}>{date_str}</td>"
                      f"<td {td}>{eps_est}</td>"
                      f"<td {td}>{eps_rep}</td>"
                      f"<td {tdc}>{surp}</td>"
                      f"</tr>")

    th = 'style="padding:10px 12px;text-align:left;font-size:11px;color:#6366f1;font-weight:700;letter-spacing:1px;background:#f8f9ff"'
    table = (f'<div style="border:1px solid rgba(99,102,241,.1);border-radius:12px;overflow:hidden;margin-top:8px">'
             f'<table style="width:100%;border-collapse:collapse">'
             f'<thead><tr>'
             f'<th {th}>DATE</th><th {th}>EPS ESTIMATE</th>'
             f'<th {th}>REPORTED EPS</th><th {th}>SURPRISE</th>'
             f'</tr></thead><tbody>{rows_html}</tbody></table></div>')
    st.markdown(table, unsafe_allow_html=True)


# ── Insiders Tab ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_insiders(ticker: str):
    import time as _t
    obj = yf.Ticker(ticker)
    for _attempt in range(3):
        try:
            df = obj.insider_transactions
            if df is not None and not df.empty:
                return df
            # Fallback: newer yfinance API
            try:
                df2 = obj.get_insider_transactions()
                if df2 is not None and not df2.empty:
                    return df2
            except Exception:
                pass
            return df
        except Exception as _e:
            _msg = str(_e).lower()
            if ("too many requests" in _msg or "429" in _msg or "rate limit" in _msg) \
                    and _attempt < 2:
                _t.sleep(3 * (2 ** _attempt))
                continue
            return None
    return None


def build_insiders(ticker: str) -> None:
    with st.spinner("Loading insider transactions..."):
        df = _fetch_insiders(ticker)
    if df is None or df.empty:
        st.info("No insider transactions found.")
        return

    df = df.copy()
    date_col = next((c for c in df.columns if "date" in c.lower()), None)
    if date_col:
        df = df.sort_values(date_col, ascending=False)

    # Summary: buys vs sells in last 6 months
    six_mo = pd.Timestamp(datetime.now() - timedelta(days=180))
    buys = sells = 0
    # Detect transaction from any likely column
    tx_col = next((c for c in df.columns if c.lower() in ("transaction", "text", "type")), None)
    for _, row in df.iterrows():
        try:
            d = row.get(date_col) if date_col else None
            in_range = (not d) or pd.Timestamp(d) >= six_mo
            if in_range:
                tx_val = ""
                for col in ([tx_col] if tx_col else []) + ["Transaction", "Text", "Type"]:
                    v = row.get(col, "")
                    if v and str(v).strip() not in ("", "None"):
                        tx_val = str(v).lower()
                        break
                if "buy" in tx_val or "purchase" in tx_val or "acquisition" in tx_val:
                    buys += 1
                elif "sell" in tx_val or "sale" in tx_val or "disposition" in tx_val:
                    sells += 1
        except Exception:
            pass

    buy_clr  = "#10b981" if buys > 0 else "#6b7280"
    sell_clr = "#ef4444" if sells > 0 else "#6b7280"
    st.markdown(
        f'<div style="font-size:13px;margin-bottom:16px;">'
        f'<span style="color:{buy_clr};font-weight:700">{buys} buys</span>'
        f' &nbsp;&middot;&nbsp; '
        f'<span style="color:{sell_clr};font-weight:700">{sells} sells</span>'
        f' <span style="color:#9ca3af">(last 6 months)</span></div>',
        unsafe_allow_html=True,
    )

    show_cols = [c for c in df.columns
                 if any(k in c.lower() for k in ["date","insider","position","transaction","shares","value","text"])]
    if not show_cols:
        show_cols = list(df.columns)
    st.dataframe(df[show_cols].head(20).reset_index(drop=True),
                 use_container_width=True, hide_index=True)



# ── HTML Presentation Generator ───────────────────────────────────────────────
def build_presentation_html(
    ticker: str,
    data: dict,
    tech: dict,
    score: int,
    horizon: str,
    hist: pd.DataFrame,
) -> str:
    """7 unique slides — only content not shown elsewhere in the app."""

    # ── value helper ─────────────────────────────────────────────────────────
    def _v(val, fmt="{:.2f}", fallback="N/A"):
        try:
            f = float(val)
            return fallback if f != f else fmt.format(f)
        except:
            return fallback

    # ── unpack data ──────────────────────────────────────────────────────────
    cname   = data["company_name"]
    sector  = data["sector"]
    price   = data["current_price"]
    prev    = data["prev_close"]
    pe      = data["pe_ratio"]
    peg     = data["peg_ratio"]
    mc      = data["mkt_cap"]
    margins = data["gross_margins"]
    cagr    = data["revenue_cagr"]
    fcfy    = data["fcf_yield"]
    rsi     = tech["rsi"]
    macd    = tech["macd_hist"]
    ma50v   = tech["ma50"]
    ma150v  = tech["ma150"]
    n_an    = data["n_analysts"]
    t_mean  = data["analyst_target_mean"]
    t_high  = data["analyst_target_high"]
    t_low   = data["analyst_target_low"]
    t_med   = data["analyst_target_median"]
    rec_key = data["rec_key"].upper().replace("_", " ")

    try:
        pct = (float(price) - float(prev)) / float(prev) * 100
    except:
        pct = float("nan")

    if score >= 80:   verdict, vcolor = "STRONG BUY", "#10b981"
    elif score >= 65: verdict, vcolor = "BUY",         "#f59e0b"
    elif score >= 45: verdict, vcolor = "HOLD",        "#f97316"
    else:             verdict, vcolor = "SELL",        "#ef4444"
    confidence = min(95, 50 + abs(score - 50))

    is_short = (horizon == "30D Tactical")
    date_str = datetime.now().strftime("%b %d, %Y")
    m_txt = fmt_pct(float(margins)) if not _isnan(float(margins)) else "N/A"
    c_txt = fmt_pct(float(cagr))    if float(cagr) != 0           else "N/A"
    ceo_s = (f"{cname} is a {sector} company scoring "
             f"<strong style='color:{vcolor}'>{score}/100</strong> — reflecting "
             f"{'exceptional' if score>=75 else 'solid' if score>=55 else 'moderate'} "
             f"positioning. Gross margins {m_txt} · Revenue CAGR {c_txt}.")

    try:
        upside = (float(t_mean) - float(price)) / float(price) * 100
        upside_str   = f'{("+" if upside >= 0 else "")}{upside:.1f}%'
        upside_color = "#10b981" if upside >= 0 else "#ef4444"
    except:
        upside_str = "N/A"; upside_color = "#94a3b8"

    # ── shared dark Plotly layout ─────────────────────────────────────────────
    _dk = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,10,22,0.92)",
        font=dict(color="#94a3b8", family="Inter,sans-serif"),
        height=340,
        margin=dict(l=52, r=22, t=22, b=44),
        xaxis=dict(gridcolor="rgba(99,102,241,.07)",
                   tickfont=dict(color="#64748b", size=11), showgrid=False, zeroline=False),
        yaxis=dict(gridcolor="rgba(99,102,241,.12)",
                   tickfont=dict(color="#64748b", size=11), zeroline=False),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11),
                    orientation="h", x=0, y=1.14),
        bargap=0.30,
    )

    def _embed(fig, first=False):
        return fig.to_html(full_html=False,
                           include_plotlyjs="cdn" if first else False,
                           config={"displayModeBar": False})

    def _slide_titled(title, inner, sub=""):
        sub_h = (f'<span style="font-size:12px;color:#334155;font-weight:400;'
                 f'margin-left:12px;letter-spacing:.5px">{sub}</span>') if sub else ""
        return (
            f'\n<section data-background="#0b0b1a">\n'
            f'<div style="padding:0 6px">'
            f'<div style="display:flex;align-items:baseline;gap:0;margin-bottom:14px;'
            f'padding-bottom:11px;border-bottom:1px solid rgba(99,102,241,.18)">'
            f'<h2 style="color:#f1f5f9;font-size:23px;font-weight:700;margin:0">{title}</h2>'
            f'{sub_h}</div>'
            f'<div style="background:rgba(99,102,241,.035);border-radius:12px;'
            f'border:1px solid rgba(99,102,241,.11);padding:6px;overflow:hidden">'
            f'{inner}</div></div>\n</section>'
        )

    def _fallback(title, sub=""):
        msg = ('<p style="color:#334155;text-align:center;padding:80px 0;font-size:14px">'
               'Data not available</p>')
        return _slide_titled(title, msg, sub=sub)

    # ── fetch annual financials ───────────────────────────────────────────────
    def _ts(df, *labels):
        if df is None or df.empty: return None
        for lbl in labels:
            if lbl in df.index:
                s = df.loc[lbl].dropna().sort_index()
                if len(s) >= 2: return s
        return None

    try:
        _inc, _bal, _cf = _fetch_financials(ticker)
    except Exception:
        _inc = _bal = _cf = None

    rev_s = _ts(_inc, "Total Revenue", "Revenue")
    ni_s  = _ts(_inc, "Net Income", "Net Income Common Stockholders")
    gp_s  = _ts(_inc, "Gross Profit")
    oi_s  = _ts(_inc, "Operating Income", "EBIT")
    eps_s = _ts(_inc, "Basic EPS", "Diluted EPS")
    fcf_s = _ts(_cf,  "Free Cash Flow")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 1 — Cover
    # ══════════════════════════════════════════════════════════════
    slide1 = f"""
<section data-background="linear-gradient(150deg,#07071a 0%,#0e0e28 55%,#091220 100%)">
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:100%;gap:22px;padding:16px">
  <div style="display:flex;align-items:center;gap:11px">
    <div style="width:42px;height:42px;background:linear-gradient(135deg,#6366f1,#8b5cf6);
                border-radius:11px;display:flex;align-items:center;justify-content:center;
                font-size:21px;font-weight:900;color:#fff;
                box-shadow:0 0 28px rgba(99,102,241,.55),0 4px 16px rgba(0,0,0,.5)">E</div>
    <div>
      <div style="font-size:10px;font-weight:700;color:#6366f1;letter-spacing:3.5px;
                  text-transform:uppercase">Eden Sovereign</div>
      <div style="font-size:9px;color:#1e293b;letter-spacing:2px;text-transform:uppercase">Intelligence Terminal</div>
    </div>
  </div>
  <div style="text-align:center;margin-top:4px">
    <div style="font-family:'JetBrains Mono',monospace;font-size:84px;font-weight:900;
                color:#f1f5f9;letter-spacing:-4px;line-height:1;
                text-shadow:0 0 70px rgba(99,102,241,.28)">{ticker}</div>
    <div style="font-size:17px;color:#475569;font-weight:400;margin-top:8px;letter-spacing:.3px">{cname}</div>
  </div>
  <div style="background:{vcolor}14;border:1.5px solid {vcolor}44;border-radius:28px;
              padding:9px 28px;box-shadow:0 0 35px {vcolor}18;margin-top:4px">
    <span style="font-family:'JetBrains Mono',monospace;font-size:21px;font-weight:800;
                 color:{vcolor};letter-spacing:.5px">&#9889; {score} &nbsp;&middot;&nbsp; {verdict}</span>
  </div>
  <div style="display:flex;gap:16px;align-items:center;font-size:12px;color:#1e293b;margin-top:2px">
    <span style="background:rgba(99,102,241,.1);color:#6366f1;padding:3px 13px;
                 border-radius:14px;font-size:11px;border:1px solid rgba(99,102,241,.2)">{sector}</span>
    <span style="color:#1e293b">{horizon}</span>
    <span style="color:#0f172a">&middot;</span>
    <span style="color:#1e293b">{date_str}</span>
  </div>
</div>
</section>"""

    # ══════════════════════════════════════════════════════════════
    # SLIDE 2 — Revenue & Net Income (annual bar)
    # ══════════════════════════════════════════════════════════════
    try:
        if rev_s is None and ni_s is None: raise ValueError
        fig2 = go.Figure(layout=_dk)
        if rev_s is not None:
            fig2.add_trace(go.Bar(
                x=[str(d)[:4] for d in rev_s.index],
                y=[v / 1e9 for v in rev_s.values],
                name="Revenue ($B)", marker_color="#6366f1",
                marker_line_color="rgba(99,102,241,.25)", marker_line_width=1,
                text=[f"${v/1e9:.1f}B" for v in rev_s.values],
                textposition="outside", textfont=dict(size=10, color="#818cf8"),
            ))
        if ni_s is not None:
            fig2.add_trace(go.Bar(
                x=[str(d)[:4] for d in ni_s.index],
                y=[v / 1e9 for v in ni_s.values],
                name="Net Income ($B)",
                marker_color=["#10b981" if v >= 0 else "#ef4444" for v in ni_s.values],
                marker_line_width=0,
                text=[f"${v/1e9:.1f}B" for v in ni_s.values],
                textposition="outside", textfont=dict(size=10, color="#6ee7b7"),
            ))
        fig2.update_layout(barmode="group",
                           yaxis=dict(title="Billion USD", gridcolor="rgba(99,102,241,.12)",
                                      tickfont=dict(color="#64748b", size=11),
                                      zeroline=True, zerolinecolor="rgba(99,102,241,.22)"))
        slide2 = _slide_titled("Revenue &amp; Net Income", _embed(fig2, first=True), sub="Annual · $B")
    except Exception:
        slide2 = _fallback("Revenue &amp; Net Income", sub="Annual · $B")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 3 — Profit Margins (annual line)
    # ══════════════════════════════════════════════════════════════
    try:
        if rev_s is None: raise ValueError
        fig3 = go.Figure(layout=_dk)
        added = 0
        if gp_s is not None:
            idx = sorted(set(gp_s.index) & set(rev_s.index))
            if len(idx) >= 2:
                gm = [float(gp_s.loc[i]) / float(rev_s.loc[i]) * 100 for i in idx]
                fig3.add_trace(go.Scatter(
                    x=[str(i)[:4] for i in idx], y=gm,
                    mode="lines+markers+text", name="Gross Margin",
                    line=dict(color="#6366f1", width=3),
                    marker=dict(size=10, color="#6366f1", line=dict(color="#0b0b1a", width=2)),
                    text=[f"{v:.1f}%" for v in gm], textposition="top center",
                    textfont=dict(size=11, color="#818cf8"),
                )); added += 1
        if oi_s is not None:
            idx2 = sorted(set(oi_s.index) & set(rev_s.index))
            if len(idx2) >= 2:
                om = [float(oi_s.loc[i]) / float(rev_s.loc[i]) * 100 for i in idx2]
                fig3.add_trace(go.Scatter(
                    x=[str(i)[:4] for i in idx2], y=om,
                    mode="lines+markers+text", name="Operating Margin",
                    line=dict(color="#f59e0b", width=3, dash="dot"),
                    marker=dict(size=10, color="#f59e0b", line=dict(color="#0b0b1a", width=2)),
                    text=[f"{v:.1f}%" for v in om], textposition="bottom center",
                    textfont=dict(size=11, color="#fbbf24"),
                )); added += 1
        if added == 0: raise ValueError
        fig3.add_hline(y=0, line_dash="dash", line_color="rgba(148,163,184,.18)", line_width=1)
        fig3.update_layout(yaxis=dict(title="Margin %", ticksuffix="%",
                                      gridcolor="rgba(99,102,241,.12)",
                                      tickfont=dict(color="#64748b", size=11)))
        slide3 = _slide_titled("Profit Margins Over Time", _embed(fig3), sub="Annual %")
    except Exception:
        slide3 = _fallback("Profit Margins Over Time", sub="Annual %")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 4 — EPS & Free Cash Flow (dual axis)
    # ══════════════════════════════════════════════════════════════
    try:
        if eps_s is None and fcf_s is None: raise ValueError
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        fig4.update_layout(**_dk)
        if eps_s is not None:
            fig4.add_trace(go.Bar(
                x=[str(d)[:4] for d in eps_s.index], y=list(eps_s.values),
                name="EPS ($)",
                marker_color=["#818cf8" if v >= 0 else "#ef4444" for v in eps_s.values],
                marker_line_width=0,
                text=[f"${v:.2f}" for v in eps_s.values],
                textposition="outside", textfont=dict(size=10, color="#a5b4fc"),
            ), secondary_y=False)
        if fcf_s is not None:
            fig4.add_trace(go.Scatter(
                x=[str(d)[:4] for d in fcf_s.index], y=[v / 1e9 for v in fcf_s.values],
                name="FCF ($B)", mode="lines+markers",
                line=dict(color="#10b981", width=3),
                marker=dict(size=10, color="#10b981", line=dict(color="#0b0b1a", width=2)),
            ), secondary_y=True)
        fig4.update_yaxes(title_text="EPS ($)", gridcolor="rgba(99,102,241,.12)",
                          tickfont=dict(color="#64748b", size=11),
                          zeroline=True, zerolinecolor="rgba(99,102,241,.22)",
                          secondary_y=False)
        fig4.update_yaxes(title_text="FCF ($B)", gridcolor="rgba(0,0,0,0)",
                          tickfont=dict(color="#64748b", size=11), secondary_y=True)
        slide4 = _slide_titled("EPS &amp; Free Cash Flow", _embed(fig4), sub="Annual")
    except Exception:
        slide4 = _fallback("EPS &amp; Free Cash Flow", sub="Annual")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 5 — Score Radar (not shown anywhere else in app)
    # ══════════════════════════════════════════════════════════════
    def _sub(val, lo, hi):
        try:
            f = float(val)
            return 40.0 if f != f else float(min(100, max(0, (f - lo) / (hi - lo) * 100)))
        except: return 40.0

    growth_s = _sub(cagr,    0.0,  0.30)
    profit_s = _sub(margins, 0.0,  0.50)
    cash_s   = _sub(fcfy,    0.0,  0.08)
    rsi_s    = _sub(rsi,     30.0, 70.0)
    val_s    = (100 - _sub(float(pe), 10, 60)) if not _isnan(float(pe)) and float(pe) > 0 else 50.0
    peg_s    = _sub((3 - float(peg)) if not _isnan(float(peg)) and float(peg) > 0 else 0, 0, 3)

    dims = ["Growth", "Profitability", "Cash Flow", "Technical", "Valuation", "PEG"]
    vals = [growth_s, profit_s, cash_s, rsi_s, val_s, peg_s]

    try:
        fig5 = go.Figure()
        fig5.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=dims + [dims[0]],
            fill="toself", name="Score",
            line=dict(color="#6366f1", width=2.5),
            fillcolor="rgba(99,102,241,.17)",
            marker=dict(size=8, color="#818cf8", line=dict(color="#0b0b1a", width=1.5)),
        ))
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", family="Inter,sans-serif"),
            height=340, margin=dict(l=36, r=36, t=18, b=18),
            showlegend=False,
            polar=dict(
                bgcolor="rgba(10,10,22,0.92)",
                angularaxis=dict(tickfont=dict(size=12, color="#94a3b8"),
                                 gridcolor="rgba(99,102,241,.14)",
                                 linecolor="rgba(99,102,241,.18)"),
                radialaxis=dict(visible=True, range=[0, 100],
                                gridcolor="rgba(99,102,241,.14)",
                                tickfont=dict(size=9, color="#334155"),
                                tickvals=[25, 50, 75, 100]),
            ),
        )
        slide5 = _slide_titled("Score Breakdown", _embed(fig5),
                                sub="Multi-factor radar · 0–100 per dimension")
    except Exception:
        slide5 = _fallback("Score Breakdown")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 6 — Analyst Price Target Range (not shown elsewhere)
    # ══════════════════════════════════════════════════════════════
    try:
        pts = {k: float(v) for k, v in
               {"Low": t_low, "Median": t_med, "Mean": t_mean, "High": t_high}.items()
               if not _isnan(float(v))}
        if len(pts) < 2: raise ValueError
        all_p  = list(pts.values()) + [float(price)]
        rng_lo = min(all_p) * 0.93
        rng_hi = max(all_p) * 1.07

        fig6 = go.Figure()
        # Shaded range band
        if "Low" in pts and "High" in pts:
            fig6.add_shape(type="rect",
                x0=pts["Low"], x1=pts["High"], y0=0.28, y1=0.72,
                line=dict(color="rgba(99,102,241,.25)", width=1),
                fillcolor="rgba(99,102,241,.07)")
        # Target markers
        colors  = {"Low": "#ef4444", "Median": "#f59e0b", "Mean": "#6366f1", "High": "#10b981"}
        symbols = {"Low": "triangle-right", "Median": "diamond", "Mean": "circle", "High": "triangle-left"}
        tpos    = {"Low": "bottom center", "Median": "top center",
                   "Mean": "top center", "High": "bottom center"}
        for lbl, val in pts.items():
            fig6.add_trace(go.Scatter(
                x=[val], y=[0.5], mode="markers+text",
                marker=dict(size=18, color=colors[lbl], symbol=symbols[lbl],
                            line=dict(color="#0b0b1a", width=2)),
                text=[f"<b>{lbl}</b><br>${val:.0f}"],
                textposition=tpos[lbl], textfont=dict(size=11, color=colors[lbl]),
                name=lbl,
            ))
        # Current price star
        cur = float(price)
        fig6.add_trace(go.Scatter(
            x=[cur], y=[0.5], mode="markers+text",
            marker=dict(size=20, color="#f59e0b", symbol="star",
                        line=dict(color="#0b0b1a", width=2)),
            text=[f"<b>Now</b><br>${cur:.0f}"],
            textposition="top center", textfont=dict(size=11, color="#f59e0b"),
            name="Current",
        ))
        fig6.add_vline(x=cur, line_dash="dot",
                       line_color="rgba(245,158,11,.35)", line_width=2)
        fig6.update_layout(
            **{**_dk, "height": 270,
               "xaxis": dict(range=[rng_lo, rng_hi], tickprefix="$",
                             gridcolor="rgba(99,102,241,.1)",
                             tickfont=dict(color="#64748b", size=11),
                             showgrid=True, zeroline=False),
               "yaxis": dict(visible=False, range=[0, 1]),
               "legend": dict(bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#94a3b8", size=11),
                              orientation="h", x=0.5, xanchor="center", y=1.12),
            }
        )
        c_clr = {"strong buy":"#10b981","buy":"#10b981","hold":"#f59e0b",
                  "sell":"#ef4444","underperform":"#ef4444"}.get(rec_key.lower(), "#6366f1")
        info = (f'<div style="display:flex;gap:18px;justify-content:center;margin-top:10px;'
                f'font-size:13px;color:#475569;flex-wrap:wrap">'
                f'<span>Consensus: <b style="color:{c_clr}">{rec_key}</b></span>'
                f'<span>·</span><span>{n_an} analysts</span><span>·</span>'
                f'<span>Upside: <b style="color:{upside_color}">{upside_str}</b></span></div>')
        slide6 = _slide_titled("Analyst Price Targets",
                               _embed(fig6) + info,
                               sub=f"{n_an} analysts · Wall St. consensus")
    except Exception:
        slide6 = _fallback("Analyst Price Targets")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 7 — Verdict
    # ══════════════════════════════════════════════════════════════
    slide7 = f"""
<section data-background="linear-gradient(150deg,#07071a 0%,#0d0d25 55%,#09111e 100%)">
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:100%;gap:16px;padding:16px;text-align:center">
  <div style="font-size:10px;font-weight:700;color:#1e293b;letter-spacing:3.5px;
              text-transform:uppercase;margin-bottom:2px">Sovereign Verdict</div>
  <div style="font-size:78px;font-weight:900;color:{vcolor};letter-spacing:-2.5px;
              text-shadow:0 0 55px {vcolor}44;line-height:1.1">{verdict}</div>
  <div style="display:flex;gap:22px;align-items:center;
              font-family:'JetBrains Mono',monospace;margin-top:4px">
    <div style="text-align:center">
      <div style="font-size:34px;font-weight:800;color:#f1f5f9">{score}</div>
      <div style="font-size:9px;color:#334155;letter-spacing:1.2px;
                  text-transform:uppercase;margin-top:3px">/ 100</div>
    </div>
    <div style="width:1px;height:44px;background:rgba(99,102,241,.18)"></div>
    <div style="text-align:center">
      <div style="font-size:34px;font-weight:800;color:#818cf8">{confidence}%</div>
      <div style="font-size:9px;color:#334155;letter-spacing:1.2px;
                  text-transform:uppercase;margin-top:3px">Confidence</div>
    </div>
    <div style="width:1px;height:44px;background:rgba(99,102,241,.18)"></div>
    <div style="text-align:center">
      <div style="font-size:16px;font-weight:700;color:#64748b">{horizon}</div>
      <div style="font-size:9px;color:#334155;letter-spacing:1.2px;
                  text-transform:uppercase;margin-top:3px">Horizon</div>
    </div>
  </div>
  <div style="max-width:620px;font-size:14px;color:#475569;line-height:1.85;
              padding:16px 22px;background:rgba(99,102,241,.05);border-radius:12px;
              border-left:3px solid {vcolor}88;text-align:left;margin-top:6px">
    {ceo_s}
  </div>
  <div style="font-size:10px;color:#0f172a;margin-top:6px">
    Eden Sovereign Intelligence Terminal &nbsp;&middot;&nbsp; {date_str}
  </div>
</div>
</section>"""

    # ══════════════════════════════════════════════════════════════
    # ASSEMBLE
    # ══════════════════════════════════════════════════════════════
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{ticker} — Eden Sovereign</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/theme/black.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root{{--r-background-color:#07071a;--r-main-font:Inter,sans-serif;
         --r-heading-font:Inter,sans-serif;--r-link-color:#6366f1}}
  .reveal{{font-family:'Inter',sans-serif}}
  .reveal h1,.reveal h2,.reveal h3{{text-transform:none;font-weight:700}}
  .reveal .slides section{{padding:26px 42px;box-sizing:border-box}}
  .reveal .progress span{{background:#6366f1}}
  .reveal .controls{{color:#6366f1}}
  body{{background:#07071a}}
</style>
</head>
<body>
<div class="reveal"><div class="slides">
{slide1}
{slide2}
{slide3}
{slide4}
{slide5}
{slide6}
{slide7}
</div></div>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/reveal.js"></script>
<script>
Reveal.initialize({{hash:true,transition:'slide',transitionSpeed:'fast',
  backgroundTransition:'fade',progress:true,controls:true,slideNumber:'c/t',plugins:[]}});
</script>
</body>
</html>"""




# ── Stock Video Generator (Remotion) ─────────────────────────────────────────
import subprocess, json as _json
from pathlib import Path as _Path

def _node_available() -> bool:
    """Return True if Node.js is installed."""
    try:
        r = subprocess.run(["node", "--version"], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def _safe_float(v, default=0.0) -> float:
    try:
        f = float(v)
        return default if f != f else f
    except Exception:
        return default


def _logo_candidates(ticker: str, info: dict) -> list:
    """Return ordered list of logo URL candidates for a ticker."""
    candidates = []
    # 1. yfinance logo_url (most accurate when present)
    yf = info.get("logo_url", "") or ""
    if yf and not yf.startswith("data:"):
        candidates.append(yf)
    # 2. Financial Modeling Prep — free PNG by ticker symbol
    candidates.append(f"https://financialmodelingprep.com/image-stock/{ticker}.png")
    # 3. Parqet — free PNG by symbol
    candidates.append(f"https://assets.parqet.com/logos/symbol/{ticker}?format=png")
    # 4. Clearbit from website domain
    website = info.get("website", "") or ""
    if website:
        domain = website.replace("https://", "").replace("http://", "").split("/")[0]
        if domain.startswith("www."):
            domain = domain[4:]
        if domain:
            candidates.append(f"https://logo.clearbit.com/{domain}")
    return candidates


@st.cache_data(ttl=3600, show_spinner=False)
def _logo_url(ticker: str, logo_hint: str, website: str) -> str:
    """Verify logo URLs — returns first real image (pixel content check)."""
    import requests
    from io import BytesIO
    try:
        from PIL import Image as _PIL
        _pil_ok = True
    except ImportError:
        _pil_ok = False

    _KNOWN = {
        "AAPL": "apple.com", "MSFT": "microsoft.com", "GOOGL": "google.com",
        "GOOG": "google.com", "AMZN": "amazon.com", "META": "meta.com",
        "TSLA": "tesla.com", "NVDA": "nvidia.com", "NFLX": "netflix.com",
        "IREN": "iren.com", "MSTR": "microstrategy.com", "COIN": "coinbase.com",
        "RIOT": "riotplatforms.com", "MARA": "marathondh.com",
    }

    domain = ""
    if website:
        domain = website.replace("https://", "").replace("http://", "").split("/")[0]
        if domain.startswith("www."):
            domain = domain[4:]
    if not domain:
        domain = _KNOWN.get(ticker.upper(), "")

    candidates: list = []
    if logo_hint and not logo_hint.startswith("data:"):
        candidates.append(logo_hint)
    candidates.append(f"https://financialmodelingprep.com/image-stock/{ticker}.png")
    candidates.append(f"https://assets.parqet.com/logos/symbol/{ticker}?format=png")
    candidates.append(f"https://storage.googleapis.com/iex/api/logos/{ticker}.png")
    if domain:
        candidates.append(f"https://logo.clearbit.com/{domain}")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    for url in candidates:
        try:
            r = requests.get(url, timeout=6, headers=headers)
            if r.status_code != 200:
                continue
            content = r.content
            if len(content) < 200:
                continue
            if _pil_ok:
                try:
                    img = _PIL.open(BytesIO(content)).convert("RGBA")
                    import numpy as _np
                    arr = _np.array(img)
                    mask = ~(((arr[:,:,0] > 230) & (arr[:,:,1] > 230) & (arr[:,:,2] > 230)) |
                             (arr[:,:,3] < 30))
                    rows = _np.any(mask, axis=1)
                    cols = _np.any(mask, axis=0)
                    if not rows.any() or not cols.any():
                        continue
                    content_h = int(rows.sum())
                    content_w = int(cols.sum())
                    if content_w < 24 or content_h < 24:
                        continue
                    total_px = img.size[0] * img.size[1]
                    content_px = content_w * content_h
                    if content_px / total_px < 0.08:
                        continue
                except Exception:
                    continue
            else:
                if len(content) < 500:
                    continue
            return url
        except Exception:
            continue
    return ""


def _logo_img_html(ticker: str, info: dict, size: int = 52) -> str:
    """Return an <img> tag with JS onerror chaining through all logo sources.
    Safe for use in st.markdown(unsafe_allow_html=True)."""
    sources = _logo_candidates(ticker, info)
    if not sources:
        return ""
    # Build nested onerror chain: src=s[0], onerror -> s[1] -> s[2] -> ... -> hide
    # We escape single quotes in URLs just in case
    def _esc(u):
        return u.replace("'", "%27")

    chain = "this.style.display='none'"
    for s in reversed(sources[1:]):
        chain = f"this.src='{_esc(s)}';this.onerror=function(){{  {chain}  }}"

    return (
        f'<img src="{_esc(sources[0])}" '
        f'onerror="{chain}" '
        f'style="width:{size}px;height:{size}px;border-radius:10px;'
        f'object-fit:contain;background:#fff;padding:3px;'
        f'vertical-align:middle;margin-right:10px;" />'
    )


def _ts_series(df, *labels):
    """Extract sorted annual time-series from a financial DataFrame."""
    if df is None or df.empty:
        return []
    for lbl in labels:
        if lbl in df.index:
            s = df.loc[lbl].dropna().sort_index()
            if len(s) >= 2:
                return [{"year": str(d)[:4], "value": float(v)} for d, v in zip(s.index, s.values)]
    return []


def _sub_score(val, lo, hi) -> float:
    try:
        f = float(val)
        return 40.0 if f != f else float(min(100, max(0, (f - lo) / (hi - lo) * 100)))
    except Exception:
        return 40.0


def build_video_props(ticker: str, data: dict, tech: dict, score: int, hist: pd.DataFrame) -> dict:
    """Build the JSON props dict matching the Remotion Zod schema."""
    info = data.get("info", {})
    pe   = _safe_float(data["pe_ratio"])
    peg  = _safe_float(data["peg_ratio"])
    rsi  = _safe_float(tech["rsi"], 50.0)

    if score >= 80:   verdict, vcolor = "STRONG BUY", "#10b981"
    elif score >= 65: verdict, vcolor = "BUY",         "#f59e0b"
    elif score >= 45: verdict, vcolor = "HOLD",        "#f97316"
    else:             verdict, vcolor = "SELL",        "#ef4444"

    # Price history (daily, max 252 points)
    price_hist: list = []
    if hist is not None and not hist.empty:
        step = max(1, len(hist) // 252)
        for d, row in hist.iloc[::step].iterrows():
            price_hist.append({"date": str(d)[:10], "close": float(row["Close"])})

    # Annual financials
    try:
        inc, bal, cf = _fetch_financials(ticker)
    except Exception:
        inc = bal = cf = None

    margins = _safe_float(data["gross_margins"])
    cagr    = _safe_float(data["revenue_cagr"])
    fcfy    = _safe_float(data["fcf_yield"])

    return {
        "ticker":       ticker,
        "companyName":  data.get("company_name", ticker),
        "sector":       data.get("sector", "N/A"),
        "logoUrl":      _logo_url(ticker,
                                   info.get("logo_url", "") or "",
                                   info.get("website", "") or ""),
        "score":        score,
        "verdict":      verdict,
        "vcolor":       vcolor,
        "horizon":      "1Y Strategic",
        "price":        _safe_float(data["current_price"]),
        "pctChange":    0.0,
        "marketCap":    _safe_float(data["mkt_cap"]),
        "pe":           pe if pe > 0 else 0.0,
        "peg":          peg if peg > 0 else 0.0,
        "margins":      margins,
        "cagr":         cagr,
        "fcfy":         fcfy,
        "rsi":          rsi,
        "nAnalysts":    int(_safe_float(data["n_analysts"])),
        "targetMean":   _safe_float(data["analyst_target_mean"]),
        "targetHigh":   _safe_float(data["analyst_target_high"]),
        "targetLow":    _safe_float(data["analyst_target_low"]),
        "recKey":       data.get("rec_key", "N/A").upper().replace("_", " "),
        "priceHistory": price_hist,
        "revenue":      _ts_series(inc, "Total Revenue", "Revenue"),
        "netIncome":    _ts_series(inc, "Net Income", "Net Income Common Stockholders"),
        "grossMargin":  _ts_series(inc, "Gross Profit") and _gross_margin_series(inc),
        "opMargin":     _op_margin_series(inc),
        "eps":          _ts_series(inc, "Basic EPS", "Diluted EPS"),
        "scoreGrowth":       _sub_score(cagr,    0.0,  0.30),
        "scoreProfitability":_sub_score(margins, 0.0,  0.50),
        "scoreCashFlow":     _sub_score(fcfy,    0.0,  0.08),
        "scoreTechnical":    _sub_score(rsi,     30.0, 70.0),
        "scoreValuation":    100 - _sub_score(pe, 10, 60) if pe > 0 else 50.0,
        "scorePeg":          _sub_score(3 - peg if peg > 0 else 0, 0, 3),
        "dateStr":           datetime.now().strftime("%b %d, %Y"),
        "ma50":              _safe_float(tech.get("ma50", 0)),
        "ma200":             _safe_float(tech.get("ma200", 0)),
    }


def _gross_margin_series(inc) -> list:
    """Compute gross margin % series."""
    if inc is None or inc.empty:
        return []
    rev = None
    gp  = None
    for lbl in ["Total Revenue", "Revenue"]:
        if lbl in inc.index:
            rev = inc.loc[lbl].dropna()
            break
    if "Gross Profit" in inc.index:
        gp = inc.loc["Gross Profit"].dropna()
    if rev is None or gp is None:
        return []
    idx = sorted(set(gp.index) & set(rev.index))
    return [{"year": str(d)[:4], "value": float(gp.loc[d]) / float(rev.loc[d])}
            for d in idx if float(rev.loc[d]) != 0]


def _op_margin_series(inc) -> list:
    """Compute operating margin % series."""
    if inc is None or inc.empty:
        return []
    rev = None
    oi  = None
    for lbl in ["Total Revenue", "Revenue"]:
        if lbl in inc.index:
            rev = inc.loc[lbl].dropna()
            break
    for lbl in ["Operating Income", "EBIT"]:
        if lbl in inc.index:
            oi = inc.loc[lbl].dropna()
            break
    if rev is None or oi is None:
        return []
    idx = sorted(set(oi.index) & set(rev.index))
    return [{"year": str(d)[:4], "value": float(oi.loc[d]) / float(rev.loc[d])}
            for d in idx if float(rev.loc[d]) != 0]


def render_stock_video(ticker: str, data: dict, tech: dict, score: int, hist: pd.DataFrame):
    """Export data JSON → call Remotion render → return MP4 path."""
    video_dir = _Path(__file__).parent / "video"
    pub_dir   = video_dir / "public"
    out_dir   = video_dir / "out"
    pub_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Clear logo cache so each render re-verifies with the current thresholds
    _logo_url.clear()

    props = build_video_props(ticker, data, tech, score, hist)
    json_path = pub_dir / "data.json"
    json_path.write_text(_json.dumps(props, ensure_ascii=False))

    out_file = out_dir / f"{ticker}.mp4"
    result = subprocess.run(
        ["npx", "remotion", "render", "StockVideo",
         f"--props=public/data.json",
         f"--output=out/{ticker}.mp4",
         "--log=error"],
        cwd=str(video_dir),
        capture_output=True, text=True,
        timeout=600,
        shell=True,   # required on Windows
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "Render failed")
    return str(out_file)

# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    # ── Google Login (graceful fallback) ───────────────────────────────────
    try:
        _user = st.experimental_user
        _user_email = _user.get("email", "") if _user else ""
        _user_name  = _user.get("name", "")  if _user else ""
    except Exception:
        _user = None
        _user_email = ""
        _user_name  = ""

    _account_label = (
        f"&#128100; {_user_email}" if _user_email else "&#128100; Sandbox Mode"
    )
    inject_css(account_label=_account_label, is_logged_in=bool(_user_email))

    # ── session_state defaults ─────────────────────────────────────────────
    st.session_state.setdefault("active_ticker", "AAPL")
    st.session_state.setdefault("run_best_pick", False)
    st.session_state.setdefault("best_pick_results", [])
    st.session_state.setdefault("tg_phone", "")
    st.session_state.setdefault("current_user_phone", "")

    # ── זיהוי משתמש מחובר / התנתקות ──────────────────────────────────────────
    _tg_ph = st.session_state.get("tg_phone", "")
    _expected_user = _tg_ph if (_tg_ph and _is_phone_registered(_tg_ph)) else ""
    if _expected_user != st.session_state["current_user_phone"]:
        # שינוי מצב התחברות — טען portfolio מתאים
        st.session_state["current_user_phone"] = _expected_user
        if _expected_user:
            st.session_state["portfolio"] = _load_user_portfolio(_expected_user)
        else:
            st.session_state["portfolio"] = _load_portfolio()
    elif "portfolio" not in st.session_state:
        st.session_state["portfolio"] = _load_portfolio()

    # ── בדיקת התראות מחיר Telegram (כל רענון) ────────────────────────────────
    try:
        _alert_tickers = set(
            a["ticker"] for a in _load_alerts_db().get("alerts", [])
            if not a.get("triggered")
        )
        _portfolio_tickers = set(
            h["ticker"] for h in (st.session_state.get("portfolio") or [])
        )
        _all_check_tickers = tuple(_alert_tickers | _portfolio_tickers)
        if _all_check_tickers:
            _all_prices = fetch_portfolio_prices(_all_check_tickers)
            _check_and_fire_tg_alerts(_all_prices)
    except Exception:
        pass

    # Apply pending ticker change BEFORE the selectbox widget is instantiated
    if st.session_state.get("pending_ticker"):
        _pt = st.session_state.pop("pending_ticker")
        if _pt in TICKER_LIST:
            st.session_state["ticker_selectbox"] = _pt
            st.session_state["active_ticker"] = _pt

    # ── Sidebar ────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(EDEN_LOGO, unsafe_allow_html=True)

        st.markdown("**Stock Search**")
        _ticker_idx = TICKER_LIST.index(st.session_state["active_ticker"]) \
            if st.session_state["active_ticker"] in TICKER_LIST \
            else (TICKER_LIST.index("AAPL") if "AAPL" in TICKER_LIST else 0)
        ticker = st.selectbox(
            "Search ticker",
            options=TICKER_LIST,
            index=_ticker_idx,
            label_visibility="collapsed",
            placeholder="Type to search (e.g. NVD → NVDA)",
            key="ticker_selectbox")
        st.session_state["active_ticker"] = ticker

        st.markdown("---")
        st.markdown("**Analysis Horizon**")
        horizon = st.radio(
            "Horizon", ["30D Tactical", "1Y Strategic"],
            index=0, label_visibility="collapsed",
            key="horizon_radio")

        st.markdown("**Moving Averages**")
        col1, col2 = st.columns(2)
        with col1:
            ma1 = st.number_input("MA 1", min_value=0, max_value=200, value=50,
                                  help="0 = hidden", key="ma1_input")
        with col2:
            ma2 = st.number_input("MA 2", min_value=0, max_value=200, value=200,
                                  help="0 = hidden", key="ma2_input")

        st.markdown("**Indicators**")
        selected_indicators = st.multiselect(
            "Indicators",
            options=ALL_INDS,
            default=[],
            label_visibility="collapsed",
            placeholder="Add indicators...",
            key="indicators_multi")

        st.markdown("---")

        # ── Best Pick ──────────────────────────────────────────────────────
        if st.button("⚡ Best Pick Now", use_container_width=True, type="primary",
                     key="best_pick_btn"):
            st.session_state["run_best_pick"] = True
            st.session_state["best_pick_results"] = []

        if st.session_state["run_best_pick"]:
            with st.status("Scouting the market for Alpha...", expanded=True) as _bp_status:
                st.write(f"Scanning {len(TICKER_LIST)} stocks — may take ~30s first time...")
                _bp_results = find_best_pick(horizon)
                st.session_state["best_pick_results"] = _bp_results
                st.session_state["run_best_pick"] = False
                _bp_status.update(label="Done! Best picks ready.", state="complete")

        if st.session_state["best_pick_results"]:
            _top5 = st.session_state["best_pick_results"][:5]
            st.markdown("**Top picks:**")
            for _rank, (_t, _s) in enumerate(_top5, 1):
                if _s >= 80:   _rc, _rl = "#10b981", "STRONG BUY"
                elif _s >= 65: _rc, _rl = "#f59e0b", "BUY"
                elif _s >= 45: _rc, _rl = "#f97316", "HOLD"
                else:          _rc, _rl = "#ef4444", "SELL"
                _medal = "🥇" if _rank == 1 else ("🥈" if _rank == 2 else ("🥉" if _rank == 3 else f"{_rank}."))
                st.markdown(
                    f'<div style="background:rgba(99,102,241,.05);border:1px solid rgba(99,102,241,.12);'
                    f'border-radius:10px;padding:7px 10px;margin:4px 0">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<span style="font-size:13px">{_medal} <b>{_t}</b></span>'
                    f'<span style="font-size:11px;font-family:monospace;color:#6366f1;font-weight:700">{_s}</span>'
                    f'</div>'
                    f'<div style="font-size:10px;font-weight:700;color:{_rc};margin-top:2px">{_rl}</div>'
                    f'</div>',
                    unsafe_allow_html=True)
            if st.button(f"Analyze {_top5[0][0]} Now", use_container_width=True,
                         key="analyze_best_btn"):
                st.session_state["pending_ticker"] = _top5[0][0]
                st.session_state["best_pick_results"] = []
                st.rerun()

        # ── 👤 חשבון משתמש + 🔔 התראות מחיר — Telegram ──────────────────────
        st.markdown("---")
        _cu = st.session_state.get("current_user_phone", "")
        if _cu:
            # ── מחובר — הצג שם + כפתור התנתקות ──────────────────────────
            _db_reg = _load_alerts_db().get("registrations", {}).get(_cu, {})
            _disp = _db_reg.get("display_phone", f"+{_cu}")
            _uc1, _uc2 = st.columns([3, 1])
            with _uc1:
                st.markdown(f"**👤 {_disp}**")
            with _uc2:
                if st.button("יציאה", key="logout_btn", use_container_width=True):
                    st.session_state["tg_phone"] = ""
                    st.session_state["current_user_phone"] = ""
                    st.session_state["portfolio"] = _load_portfolio()
                    st.rerun()
            st.markdown("**🔔 התראות מחיר**")
        else:
            st.markdown("**🔔 התחברות / התראות מחיר**")

        _tg_phone = st.text_input(
            "מספר טלפון",
            value=st.session_state["tg_phone"],
            placeholder="Enter phone number",
            key="tg_phone_input",
            label_visibility="collapsed",
        )
        if _tg_phone != st.session_state["tg_phone"]:
            st.session_state["tg_phone"] = _tg_phone

        _tg_configured = bool(_tg_token())
        _bot_name = st.secrets.get("TELEGRAM_BOT_NAME", "@eden_alerts_bot")

        if not _tg_configured:
            st.markdown(
                "**הגדרה נדרשת (פעם אחת):**\n\n"
                "1. פתח טלגרם → `@BotFather`\n"
                "2. שלח `/newbot` → קבל token\n"
                "3. הכנס ב-`.streamlit/secrets.toml`:\n\n"
                "```\nTELEGRAM_BOT_TOKEN = \"...\"\n```\n\n"
                "4. הפעל מחדש את Streamlit"
            )
        elif _tg_phone and len(_normalize_phone(_tg_phone)) >= 7:
            _norm = _normalize_phone(_tg_phone)
            if _is_phone_registered(_tg_phone):
                st.success(f"✅ {_tg_phone} — מחובר לטלגרם")
                # ── בדוק אם יש הודעות רישום חדשות ─────────────────────────
                _poll_telegram_registrations()

                # ── טופס הוספת התראה ──────────────────────────────────────
                _ac1, _ac2 = st.columns(2)
                with _ac1:
                    _alert_ticker = st.text_input(
                        "טיקר", placeholder="NVDA",
                        key="alert_ticker_input",
                        label_visibility="visible",
                    ).strip().upper()
                with _ac2:
                    _alert_cond = st.selectbox(
                        "תנאי", ["מעל", "מתחת", "שווה ל"],
                        key="alert_cond_select",
                        label_visibility="visible",
                    )
                _alert_price = st.number_input(
                    "מחיר יעד ($)", min_value=0.01, value=100.0,
                    step=1.0, key="alert_price_input",
                )
                if st.button("➕ הוסף התראה", use_container_width=True, key="add_alert_btn"):
                    if _alert_ticker:
                        _cond_en = "above" if _alert_cond == "מעל" else ("equals" if _alert_cond == "שווה ל" else "below")
                        if _add_tg_alert(_tg_phone, _alert_ticker, _cond_en, _alert_price):
                            st.toast(f"✅ התראה נוספה: {_alert_ticker} {_alert_cond} ${_alert_price:,.2f}")
                        else:
                            st.toast("שגיאה בהוספת התראה")

                # ── רשימת התראות פעילות ───────────────────────────────────
                _active = [a for a in _list_tg_alerts(_tg_phone) if not a.get("triggered")]
                if _active:
                    st.markdown("**התראות פעילות:**")
                    for _ai, _al in enumerate(_active):
                        _dir = "מעל" if _al["condition"] == "above" else ("שווה ל" if _al["condition"] == "equals" else "מתחת")
                        _col_a, _col_b = st.columns([4, 1])
                        with _col_a:
                            st.caption(f"• {_al['ticker']} {_dir} ${_al['target_price']:,.2f}")
                        with _col_b:
                            if st.button("🗑", key=f"del_alert_{_ai}"):
                                _delete_tg_alert(_tg_phone, _ai)
                                st.rerun()
            else:
                # ── לא רשום — Deep Link אוטומטי ───────────────────────────
                _bot_username = _bot_name.lstrip("@")
                _deep_link = f"https://t.me/{_bot_username}?start={_norm}"
                st.markdown(
                    f'<a href="{_deep_link}" target="_blank" style="'
                    f'display:block;text-align:center;background:#229ED9;color:#fff;'
                    f'padding:10px;border-radius:8px;font-weight:600;font-size:14px;'
                    f'text-decoration:none;margin-bottom:8px;">'
                    f'📲 הירשם דרך טלגרם</a>',
                    unsafe_allow_html=True,
                )
                st.caption("לחץ → טלגרם נפתח → לחץ START → חזור לכאן")
                if st.button("✅ בדוק רישום", use_container_width=True, key="check_reg_btn"):
                    with st.spinner("בודק..."):
                        _poll_telegram_registrations()
                    if _is_phone_registered(_tg_phone):
                        st.toast("✅ נרשמת בהצלחה!")
                        st.rerun()
                    else:
                        st.warning("עדיין לא נמצא. לחץ START בטלגרם ונסה שוב.")

        st.markdown("---")
        st.caption("⚠️ For educational purposes only. Not financial advice.")

    # ── Auto-analyze (no button needed) ──────────────────────────────────
    with st.spinner(f"Analyzing {ticker}..."):
        data = fetch_data(ticker)

    if data["error"] and data["hist"].empty:
        st.error(f"Failed to retrieve data for **{ticker}**: {data['error']}")
        return

    hist = data["hist"]
    if hist.empty:
        st.warning(f"No price history for **{ticker}**. The ticker may be invalid or delisted.")
        return

    tech     = compute_technicals(hist)
    is_etf   = data.get("is_etf", False)
    score    = compute_score(data, tech, horizon) if not is_etf else 0

    # ── Header ─────────────────────────────────────────────────────────────
    _info = data.get("info", {})
    _verified_logo = _logo_url(ticker, _info.get("logo_url", "") or "", _info.get("website", "") or "")
    _logo_html = (
        f'<img src="{_verified_logo}" '
        f'style="width:52px;height:52px;border-radius:10px;object-fit:contain;'
        f'background:#fff;padding:3px;vertical-align:middle;margin-right:10px;" />'
    ) if _verified_logo else ""
    st.markdown(
        f'<div class="ticker-header" style="align-items:center;">'
        f'{_logo_html}'
        f'<span class="ticker-symbol">{ticker}</span>'
        f'<span class="company-full">{data["company_name"]}</span>'
        f'{score_badge_html(score, is_etf=is_etf)}'
        f'</div>'
        f'<div style="color:#9ca3af;font-size:12px;margin-bottom:16px;">'
        f'{data["sector"]} &nbsp;·&nbsp; {horizon} &nbsp;·&nbsp; '
        f'Updated {datetime.now().strftime("%H:%M:%S")}</div>',
        unsafe_allow_html=True)


    render_metric_cards(data, tech)
    if not is_etf:
        render_analyst_card(data)

    # ── Tabs ────────────────────────────────────────────────────────────────
    _video_enabled = _node_available()
    _tab_names = ["📈 Chart", "📋 Report", "🔎 Peers", "📰 News", "📊 Financials",
                  "📅 Earnings", "👔 Insiders"]
    if _video_enabled:
        _tab_names.append("🎬 Video")
    _tab_names.append("💼 Portfolio")
    _tabs = st.tabs(_tab_names)
    tab_chart, tab_rep, tab_peers, tab_news, tab_fin, tab_earn, tab_ins = _tabs[:7]
    if _video_enabled:
        tab_slides = _tabs[7]
        tab_portfolio = _tabs[8]
    else:
        tab_slides = None
        tab_portfolio = _tabs[7]

    with tab_chart:
        if len(hist) < 5:
            st.warning("Not enough price history to render chart.")
        else:
            fig = build_chart(hist, tech, int(ma1), int(ma2), selected_indicators)
            st.plotly_chart(fig, config={"displayModeBar": False}, use_container_width=True)

    with tab_rep:
        if is_etf:
            info = data["info"]
            _td = lambda v: "N/A" if v is None else v
            cat  = _td(info.get("category") or info.get("fundFamily"))
            aum  = info.get("totalAssets")
            aum_str = fmt_mcap(float(aum)) if aum else "N/A"
            exp  = info.get("annualReportExpenseRatio") or info.get("expenseRatio")
            exp_str = f"{float(exp)*100:.2f}%" if exp else "N/A"
            ytd  = info.get("ytdReturn")
            ytd_str = f"{float(ytd)*100:.1f}%" if ytd else "N/A"
            desc = info.get("longBusinessSummary") or "No description available."
            st.markdown(f"""
<div class="exec-card">
  <div class="ceo-summary">
    <div class="ceo-summary-title">&#9673; ETF / FUND OVERVIEW</div>
    <p>{desc[:600]}{"..." if len(desc)>600 else ""}</p>
  </div>
  <div class="report-section">
    <div class="report-section-title">Fund Details</div>
    <div class="rpt-row"><span class="rpt-name">Category</span><span class="rpt-value">{cat}</span></div>
    <div class="rpt-row"><span class="rpt-name">AUM</span><span class="rpt-value">{aum_str}</span></div>
    <div class="rpt-row"><span class="rpt-name">Expense Ratio</span><span class="rpt-value">{exp_str}</span></div>
    <div class="rpt-row"><span class="rpt-name">YTD Return</span><span class="rpt-value">{ytd_str}</span></div>
  </div>
  <div class="verdict-box">
    <span class="verdict-label" style="color:#6366f1;">ETF / FUND</span>
    <div class="verdict-meta">Fundamental scoring not applicable to funds.<br>Analysis based on price action only.</div>
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(build_report(ticker, data, tech, score, horizon), unsafe_allow_html=True)

            # ── Monte Carlo Price Simulation ─────────────────────────────────
            st.markdown("---")
            st.markdown(
                '<div style="font-size:13px;font-weight:700;color:#6366f1;'
                'letter-spacing:.08em;margin-bottom:4px;">&#127922; MONTE CARLO PRICE SIMULATION</div>'
                '<div style="font-size:11px;color:#9ca3af;margin-bottom:12px;">'
                '1,000 Geometric Brownian Motion paths · Calibrated to 1-year historical volatility</div>',
                unsafe_allow_html=True,
            )
            with st.spinner("מריץ סימולציה..."):
                _mc = run_monte_carlo(hist, data.get("current_price", 0))

            if _mc:
                _s30  = _mc["s30"]
                _s365 = _mc["s365"]
                _vol  = _mc["vol_annual"] * 100

                # Summary cards
                _mc1, _mc2, _mc3 = st.columns(3)
                with _mc1:
                    st.markdown(
                        f'<div style="background:rgba(99,102,241,.07);border-radius:12px;padding:14px 18px;">'
                        f'<div style="font-size:11px;color:#9ca3af;font-weight:600;letter-spacing:.06em;">30-DAY MEDIAN</div>'
                        f'<div style="font-size:22px;font-weight:700;color:#f8fafc;margin:4px 0;">'
                        f'${_s30["median"]:,.2f}</div>'
                        f'<div style="font-size:11px;color:#6b7280;">Range: ${_s30["p10"]:,.0f} – ${_s30["p90"]:,.0f}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                with _mc2:
                    _chg = (_s365["median"] / data.get("current_price", 1) - 1) * 100
                    _chg_color = "#22c55e" if _chg >= 0 else "#ef4444"
                    st.markdown(
                        f'<div style="background:rgba(99,102,241,.07);border-radius:12px;padding:14px 18px;">'
                        f'<div style="font-size:11px;color:#9ca3af;font-weight:600;letter-spacing:.06em;">1-YEAR MEDIAN</div>'
                        f'<div style="font-size:22px;font-weight:700;color:#f8fafc;margin:4px 0;">'
                        f'${_s365["median"]:,.2f}</div>'
                        f'<div style="font-size:11px;color:{_chg_color};">{"▲" if _chg>=0 else "▼"} '
                        f'{abs(_chg):.1f}% expected</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                with _mc3:
                    st.markdown(
                        f'<div style="background:rgba(99,102,241,.07);border-radius:12px;padding:14px 18px;">'
                        f'<div style="font-size:11px;color:#9ca3af;font-weight:600;letter-spacing:.06em;">IMPLIED VOLATILITY</div>'
                        f'<div style="font-size:22px;font-weight:700;color:#f8fafc;margin:4px 0;">'
                        f'{_vol:.1f}%</div>'
                        f'<div style="font-size:11px;color:#6b7280;">Annualized · Historical</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
                st.plotly_chart(_mc["fig"], config={"displayModeBar": False},
                                use_container_width=True)
                st.caption(
                    "⚠️ סימולציה זו מבוססת על תנועת מחיר היסטורית בלבד ואינה מהווה המלצת השקעה."
                )
            else:
                st.info("אין מספיק נתוני מחיר לסימולציה.")

    with tab_peers:
        # Session-state key for custom peers per ticker
        _extra_key = f"extra_peers_{ticker}"
        if _extra_key not in st.session_state:
            st.session_state[_extra_key] = []
        extra_tuple = tuple(st.session_state[_extra_key])

        peer_list = get_peers_for(ticker)
        if not peer_list and not extra_tuple:
            st.info(f"No peer group found for **{ticker}**. Use the search below to add stocks manually.")
        else:
            with st.spinner("Fetching peer data..."):
                df_peers = build_peers(ticker, self_data=data, extra_peers=extra_tuple)
            if df_peers.empty:
                st.warning("Could not retrieve peer data.")
            else:
                st.caption(f"Sector peers for **{ticker}** ({data['sector']}) — ★ = selected stock")
                st.dataframe(df_peers, use_container_width=True, hide_index=True)

        # ── Add stock to comparison ────────────────────────────────────
        st.markdown("---")
        st.markdown("**&#43; הוסף מניה להשוואה**")
        _col1, _col2, _col3 = st.columns([3, 1, 1])
        with _col1:
            _add_input = st.text_input(
                "ticker_add", placeholder="הקלד טיקר (לדוג. MSFT, TSLA...)",
                label_visibility="collapsed", key=f"add_input_{ticker}",
            )
        with _col2:
            _add_btn = st.button("+ הוסף", use_container_width=True, key=f"add_btn_{ticker}")
        with _col3:
            _clear_btn = st.button("נקה הכל", use_container_width=True, key=f"clear_btn_{ticker}")

        if _add_btn and _add_input:
            sym = _add_input.strip().upper()
            if sym and sym != ticker.upper() and sym not in st.session_state[_extra_key]:
                st.session_state[_extra_key].append(sym)
                st.rerun()

        if _clear_btn:
            st.session_state[_extra_key] = []
            st.rerun()

        if st.session_state[_extra_key]:
            added_html = " ".join(
                f'<span style="background:rgba(99,102,241,.1);color:#6366f1;'
                f'padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600;">'
                f'{s}</span>'
                for s in st.session_state[_extra_key]
            )
            st.markdown(f'<div style="margin-top:6px">נוספו: {added_html}</div>',
                        unsafe_allow_html=True)

    with tab_news:
        build_news(ticker)

    with tab_fin:
        if is_etf:
            st.info("Financial statements are not applicable to ETFs/funds.")
        else:
            build_financials(ticker)

    with tab_earn:
        if is_etf:
            st.info("Earnings data is not applicable to ETFs/funds.")
        else:
            build_earnings(ticker, data["info"])

    with tab_ins:
        if is_etf:
            st.info("Insider transactions are not applicable to ETFs/funds.")
        else:
            build_insiders(ticker)

    if tab_slides is not None:
        with tab_slides:
            if is_etf:
                st.info("Video generation is available for stocks only.")
            else:
                st.markdown(
                    '<p style="color:#6b7280;font-size:13px;margin-bottom:8px">'
                    'Generates a <b>30-second HD video</b> (1920×1080) with 5 animated scenes: '
                    'Cover · Price Chart · Financials · Score Radar · Verdict.</p>',
                    unsafe_allow_html=True,
                )
                node_ok = _node_available()
                if not node_ok:
                    st.error(
                        "Node.js not found. Install from https://nodejs.org then restart the app.",
                        icon="🚫",
                    )
                else:
                    if st.button("🎬 Generate Video", type="primary",
                                 use_container_width=True, key=f"gen_vid_{ticker}"):
                        with st.spinner("Rendering 30-second video — this takes ~60 seconds..."):
                            try:
                                mp4_path = render_stock_video(ticker, data, tech, score, hist)
                                st.session_state[f"vid_{ticker}"] = mp4_path
                            except Exception as e:
                                st.error(f"Render failed: {e}")

                vid_key = f"vid_{ticker}"
                if vid_key in st.session_state:
                    mp4_path = st.session_state[vid_key]
                    try:
                        vid_bytes = open(mp4_path, "rb").read()
                        c1, c2 = st.columns([2, 1])
                        with c1:
                            st.download_button(
                                label="⬇️  Download MP4",
                                data=vid_bytes,
                                file_name=f"{ticker}_sovereign_{datetime.now().strftime('%Y%m%d')}.mp4",
                                mime="video/mp4",
                                use_container_width=True,
                                key=f"dl_vid_{ticker}",
                            )
                        with c2:
                            st.caption(f"{len(vid_bytes)//1024//1024:.1f} MB · 30s · 1080p")
                        st.video(mp4_path)
                    except Exception:
                        st.warning("Video file not found. Generate again.")

    # ── Portfolio Tab (far right) ────────────────────────────────────────────
    with tab_portfolio:
        st.markdown("### 💼 Portfolio Builder")
        usd_ils = get_usd_ils()

        # Add stock row
        _pc1, _pc2, _pc3, _pc4 = st.columns([2, 1, 1.5, 1])
        with _pc1:
            _port_ticker = st.selectbox("מניה", options=TICKER_LIST,
                                        label_visibility="collapsed",
                                        key="port_ticker_sel",
                                        placeholder="בחר מניה...")
        with _pc2:
            _port_qty = st.number_input("כמות", min_value=0.01, value=1.0,
                                        step=1.0, label_visibility="collapsed",
                                        key="port_qty")
        with _pc3:
            _port_buy = st.number_input("מחיר קנייה $", min_value=0.01, value=100.0,
                                        step=1.0, label_visibility="collapsed",
                                        key="port_buy")
        with _pc4:
            if st.button("+ הוסף", use_container_width=True, key="port_add"):
                _existing = [h["ticker"] for h in st.session_state["portfolio"]]
                if _port_ticker not in _existing:
                    st.session_state["portfolio"].append({
                        "ticker": _port_ticker,
                        "quantity": _port_qty,
                        "buy_price": _port_buy,
                    })
                    _save_portfolio(st.session_state["portfolio"])
                    st.rerun()
                else:
                    st.warning(f"{_port_ticker} כבר בתיק.")

        if st.button("&#9851; Reset Portfolio", use_container_width=False, key="port_reset"):
            st.session_state["portfolio"] = []
            _save_portfolio([])
            st.rerun()

        _portfolio = st.session_state["portfolio"]

        if not _portfolio:
            st.info("התיק ריק — הוסף מניות למעלה.")
        else:
            _tickers_tuple = tuple(h["ticker"] for h in _portfolio)
            with st.spinner("מעדכן מחירים..."):
                _prices = fetch_portfolio_prices(_tickers_tuple)

            _rows = []
            _ai_holdings = []
            for _h in _portfolio:
                _t = _h["ticker"]
                _cur = _prices.get(_t, 0.0)
                _qty = _h["quantity"]
                _buy = _h["buy_price"]
                _val_usd = _cur * _qty
                _val_ils = _val_usd * usd_ils
                _pl = (_cur - _buy) * _qty
                _pl_pct = ((_cur / _buy) - 1) * 100 if _buy else 0
                _rows.append({
                    "Ticker": _t,
                    "Qty": _qty,
                    "Buy $": f"${_buy:,.2f}",
                    "Current $": f"${_cur:,.2f}" if _cur else "N/A",
                    "Value ($)": f"${_val_usd:,.0f}",
                    "Value (₪)": f"₪{_val_ils:,.0f}",
                    "P&L $": f"{'+'if _pl>=0 else ''}{_pl:,.0f}",
                    "P&L %": f"{'+'if _pl_pct>=0 else ''}{_pl_pct:.1f}%",
                })
                try:
                    _d = fetch_data(_t)
                    _sc = compute_score(_d, compute_technicals(_d["hist"]), horizon, use_news=False) if not _d["hist"].empty else 50
                    _sector = _d.get("sector", "Unknown")
                except Exception:
                    _sc = 50
                    _sector = "Unknown"
                _ai_holdings.append({
                    "ticker": _t, "sector": _sector, "qty": _qty,
                    "value_usd": _val_usd, "score": _sc,
                })

            st.dataframe(pd.DataFrame(_rows), use_container_width=True, hide_index=True)

            _pie_labels = [r["Ticker"] for r in _rows]
            _pie_vals   = [_prices.get(h["ticker"], 0) * h["quantity"] for h in _portfolio]
            if any(v > 0 for v in _pie_vals):
                _pie_fig = go.Figure(go.Pie(
                    labels=_pie_labels, values=_pie_vals,
                    marker_colors=EDEN_COLORS[:len(_pie_labels)],
                    hole=0.45, textinfo="label+percent", textfont_size=13,
                ))
                _pie_fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=320,
                )
                st.plotly_chart(_pie_fig, config={"displayModeBar": False},
                                use_container_width=True)

            st.markdown("---")
            st.markdown("#### &#129302; ניתוח תיק")
            st.markdown(portfolio_ai_analysis(_ai_holdings, usd_ils))


if __name__ == "__main__":
    main()
