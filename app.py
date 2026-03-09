"""
Eden Sovereign Intelligence Terminal v2026
Institutional-grade equity research terminal.
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import yfinance as yf
import requests as _requests
_YF_SESSION = _requests.Session()
_YF_SESSION.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
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


# ── CSS ───────────────────────────────────────────────────────────────────────
def inject_css() -> None:
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
    </style>
    """, unsafe_allow_html=True)


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
@st.cache_data(ttl=300, show_spinner=False)
def fetch_data(ticker: str) -> dict:
    out: dict = {
        "ticker": ticker, "info": {}, "hist": pd.DataFrame(),
        "company_name": ticker, "current_price": float("nan"),
        "prev_close": float("nan"), "mkt_cap": 0.0,
        "pe_ratio": float("nan"), "forward_pe": float("nan"),
        "peg_ratio": float("nan"), "gross_margins": float("nan"),
        "fcf": float("nan"), "revenue_cagr": 0.0,
        "fcf_yield": float("nan"), "sector": "N/A", "dividend_yield": 0.0,
        "analyst_target_mean": float("nan"), "analyst_target_high": float("nan"),
        "analyst_target_low": float("nan"), "analyst_target_median": float("nan"),
        "n_analysts": 0, "rec_mean": float("nan"), "rec_key": "N/A",
        "error": None,
        "is_etf": False, "quote_type": "EQUITY",
    }
    try:
        obj = yf.Ticker(ticker, session=_YF_SESSION)
        try:
            info = obj.info or {}
        except Exception:
            info = {}
        out["info"] = info

        out["company_name"]  = info.get("longName") or info.get("shortName") or ticker
        qt = info.get("quoteType", "EQUITY").upper()
        out["quote_type"] = qt
        out["is_etf"]     = qt in ("ETF", "MUTUALFUND", "INDEX")
        # Price: try several fields in order
        _price = (info.get("currentPrice") or info.get("regularMarketPrice")
                  or info.get("navPrice") or info.get("ask") or info.get("bid"))
        out["current_price"] = float(_safe(_price, float("nan")))
        out["prev_close"]    = float(_safe(info.get("previousClose") or info.get("regularMarketPreviousClose"), float("nan")))
        out["mkt_cap"]       = float(_safe(info.get("marketCap"), 0.0))
        out["pe_ratio"]      = float(_safe(info.get("trailingPE"), float("nan")))
        out["forward_pe"]    = float(_safe(info.get("forwardPE"), float("nan")))
        out["gross_margins"] = float(_safe(info.get("grossMargins"), float("nan")))
        out["fcf"]           = float(_safe(info.get("freeCashflow"), float("nan")))
        out["sector"]        = info.get("sector") or "N/A"
        out["dividend_yield"]= float(_safe(info.get("dividendYield"), 0.0))

        # ── PEG ratio: try 4 sources ──────────────────────────────────────
        peg = _safe(info.get("pegRatio"), None)
        if peg is None or _isnan(float(peg)):
            peg = _safe(info.get("trailingPegRatio"), None)
        if peg is None or _isnan(float(peg)):
            # Calculate: P/E ÷ (earningsGrowth × 100)
            pe  = info.get("trailingPE")
            eg  = info.get("earningsGrowth")
            if pe and eg and float(pe) > 0 and float(eg) > 0:
                peg = float(pe) / (float(eg) * 100.0)
        if peg is None or _isnan(float(peg)):
            # Calculate: forwardPE ÷ (earningsQuarterlyGrowth × 100)
            fpe = info.get("forwardPE")
            eqg = info.get("earningsQuarterlyGrowth")
            if fpe and eqg and float(fpe) > 0 and float(eqg) > 0:
                peg = float(fpe) / (float(eqg) * 100.0)
        out["peg_ratio"] = float(_safe(peg, float("nan")))

        # ── Analyst data ───────────────────────────────────────────────────
        out["analyst_target_mean"]   = float(_safe(info.get("targetMeanPrice"), float("nan")))
        out["analyst_target_high"]   = float(_safe(info.get("targetHighPrice"), float("nan")))
        out["analyst_target_low"]    = float(_safe(info.get("targetLowPrice"), float("nan")))
        out["analyst_target_median"] = float(_safe(info.get("targetMedianPrice"), float("nan")))
        out["n_analysts"]            = int(_safe(info.get("numberOfAnalystOpinions"), 0))
        out["rec_mean"]              = float(_safe(info.get("recommendationMean"), float("nan")))
        out["rec_key"]               = info.get("recommendationKey") or "N/A"

        # ── FCF Yield ──────────────────────────────────────────────────────
        if out["mkt_cap"] > 0 and not _isnan(out["fcf"]):
            out["fcf_yield"] = out["fcf"] / out["mkt_cap"]

        # ── Revenue CAGR ───────────────────────────────────────────────────
        try:
            fin = obj.financials
            if fin is not None and not fin.empty:
                for lbl in ["Total Revenue", "Revenue"]:
                    if lbl in fin.index:
                        rev = fin.loc[lbl].dropna().sort_index()
                        if len(rev) >= 2:
                            oldest, latest, n = float(rev.iloc[0]), float(rev.iloc[-1]), len(rev)-1
                            if oldest > 0 and latest > 0:
                                out["revenue_cagr"] = float((latest/oldest)**(1.0/n) - 1.0)
                        break
        except Exception:
            pass

        # ── Historical prices ──────────────────────────────────────────────
        try:
            hist = obj.history(period="1y", interval="1d", auto_adjust=True)
            hist = hist.dropna(subset=["Close"])
            if hist.empty:
                hist = obj.history(
                    start=(datetime.today()-timedelta(days=400)).strftime("%Y-%m-%d"),
                    end=datetime.today().strftime("%Y-%m-%d"),
                    interval="1d", auto_adjust=True).dropna(subset=["Close"])
            out["hist"] = hist
            if _isnan(out["current_price"]) and not hist.empty:
                out["current_price"] = float(hist["Close"].iloc[-1])
            if _isnan(out["prev_close"]) and len(hist) >= 2:
                out["prev_close"] = float(hist["Close"].iloc[-2])
        except Exception as e:
            out["error"] = str(e)

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


# ── Quantum Scoring Engine ────────────────────────────────────────────────────
def compute_score(data: dict, tech: dict, horizon: str) -> int:
    price   = np.float64(_safe(data["current_price"], 100.0))
    rsi     = np.float64(tech["rsi"])
    macd    = np.float64(tech["macd_hist"])
    ma50v   = np.float64(_safe(tech["ma50"], float(price)))
    pe      = np.float64(data["pe_ratio"])
    peg     = np.float64(data["peg_ratio"])
    margins = np.float64(_safe(data["gross_margins"], 0.25))
    cagr    = np.float64(data["revenue_cagr"])
    fcfy    = np.float64(_safe(data["fcf_yield"], 0.02))
    mktcap  = np.float64(data["mkt_cap"])

    total = np.float64(0.0)

    if horizon == "30D Tactical":
        # RSI (max 35) — wide range 20-80 for fairness
        rsi_score = np.float64(np.clip((float(rsi)-20.0)/60.0*35.0, 0.0, 35.0))
        if float(rsi) > 75.0: rsi_score = np.float64(max(0.0, float(rsi_score)-8.0))
        if float(rsi) < 25.0: rsi_score = np.float64(max(0.0, float(rsi_score)-5.0))

        # MACD (max 20) — centered at 10
        denom      = np.float64(max(abs(float(price)*0.002), 1e-9))
        macd_norm  = np.float64(np.clip(float(macd)/float(denom), -1.0, 1.0))
        macd_score = np.float64(10.0 + macd_norm*10.0)

        # MA50 trend (max 10)
        if float(price) >= float(ma50v):
            ma_score = np.float64(10.0)
        else:
            below = (float(ma50v)-float(price))/max(float(ma50v),1e-9)
            ma_score = np.float64(max(0.0, 10.0 - below*120.0))

        # P/E (max 15)
        if _isnan(float(pe)) or float(pe) <= 0:
            pe_score = np.float64(7.5)
        elif float(pe) < 20:   pe_score = np.float64(15.0)
        elif float(pe) < 35:   pe_score = np.float64(15.0-(float(pe)-20.0)/15.0*7.0)
        elif float(pe) < 60:   pe_score = np.float64(8.0-(float(pe)-35.0)/25.0*5.0)
        else:                  pe_score = np.float64(3.0)

        # PEG (max 10)
        if _isnan(float(peg)) or float(peg) <= 0:
            peg_score = np.float64(5.0)
        else:
            peg_score = np.float64(np.clip((3.0-float(peg))/3.0*10.0, 0.0, 10.0))

        # CAGR bonus (max 10)
        cagr_bonus = np.float64(np.clip(float(cagr)/0.30*10.0, 0.0, 10.0))

        total = rsi_score + macd_score + ma_score + pe_score + peg_score + cagr_bonus
        if mktcap > MEGA_CAP_THRESHOLD:
            total = np.float64(max(float(total), 45.0))

    else:  # 1Y Strategic
        cagr_score   = np.float64(np.clip(float(cagr)/0.30*25.0, 0.0, 25.0))

        if _isnan(float(peg)) or float(peg) <= 0:
            peg_score = np.float64(8.0)
        else:
            peg_score = np.float64(np.clip((3.0-float(peg))/3.0*20.0, 0.0, 20.0))
            if float(peg) < 1.5: peg_score = np.float64(min(20.0, float(peg_score)+3.0))

        fcf_score    = np.float64(np.clip(float(fcfy)/0.08*20.0, 0.0, 20.0))
        margin_score = np.float64(np.clip(float(margins)/0.40*15.0, 0.0, 15.0))
        if float(margins) > 0.40: margin_score = np.float64(15.0)

        tech_score   = np.float64(np.clip((float(rsi)-20.0)/60.0*20.0, 0.0, 20.0))
        total = cagr_score + peg_score + fcf_score + margin_score + tech_score
        if mktcap > MEGA_CAP_THRESHOLD:
            total = np.float64(max(float(total), 50.0))

    return int(np.clip(float(total), 1.0, 100.0))


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
def build_peers(ticker: str, self_info: dict | None = None, extra_peers: tuple = ()) -> pd.DataFrame:
    peers = get_peers_for(ticker)
    # Merge extra_peers without duplicates
    all_peers = list(dict.fromkeys(peers + [p for p in extra_peers if p != ticker.upper()]))
    if not all_peers:
        return pd.DataFrame()
    peers = all_peers

    def _one(sym: str) -> tuple[str, dict]:
        try: return sym, yf.Ticker(sym, session=_YF_SESSION).info or {}
        except: return sym, {}

    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(_one, peers))

    def _row_from(sym: str, info: dict, is_self: bool = False) -> dict:
        mc = float(_safe(info.get("marketCap"), 0.0))
        p  = float(_safe(info.get("currentPrice") or info.get("regularMarketPrice"), float("nan")))
        pe = float(_safe(info.get("trailingPE"), float("nan")))
        pg = float(_safe(info.get("pegRatio"),   float("nan")))
        gm = float(_safe(info.get("grossMargins"), float("nan")))
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
    # Add self first
    if self_info:
        rows.append(_row_from(ticker.upper(), self_info, is_self=True))
    # Add peers
    for sym, info in results:
        rows.append(_row_from(sym, info))

    return pd.DataFrame(rows)


# ── Metric Cards ──────────────────────────────────────────────────────────────
def render_metric_cards(data: dict, tech: dict) -> None:
    price = data["current_price"]; prev = data["prev_close"]
    pct = ((float(price)-float(prev))/float(prev)*100) if (not _isnan(price) and not _isnan(prev) and float(prev)!=0) else float("nan")
    pct_cls  = "positive" if not _isnan(pct) and pct>=0 else "negative"
    pct_sign = "+" if not _isnan(pct) and pct>=0 else ""
    pe  = data["pe_ratio"]; peg = data["peg_ratio"]; mc = data["mkt_cap"]
    ma50v = tech["ma50"]
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
        <div class="metric-label">MA 50</div>
        <div class="metric-value">{fmt_price(float(ma50v)) if not _isnan(float(ma50v)) else "N/A"}</div>
        <div class="metric-sub neutral">50-Day Average</div>
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
        articles = yf.Ticker(ticker, session=_YF_SESSION).news or []
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
    obj = yf.Ticker(ticker, session=_YF_SESSION)
    try:   inc = obj.financials
    except: inc = None
    try:   bal = obj.balance_sheet
    except: bal = None
    try:   cf  = obj.cashflow
    except: cf  = None
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
    obj = yf.Ticker(ticker, session=_YF_SESSION)
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
    try:   return yf.Ticker(ticker, session=_YF_SESSION).insider_transactions
    except: return None


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
    """Verify logo URLs and return first one that is a real image (>= 80×80 px).
    Cached per ticker for 1 hour to avoid repeated HTTP calls."""
    import requests
    from io import BytesIO
    try:
        from PIL import Image as _PIL
        _pil_ok = True
    except ImportError:
        _pil_ok = False

    # Build candidate list inline (can't call _logo_candidates inside cache_data easily)
    candidates: list = []
    if logo_hint and not logo_hint.startswith("data:"):
        candidates.append(logo_hint)
    candidates.append(f"https://financialmodelingprep.com/image-stock/{ticker}.png")
    candidates.append(f"https://assets.parqet.com/logos/symbol/{ticker}?format=png")
    if website:
        domain = website.replace("https://", "").replace("http://", "").split("/")[0]
        if domain.startswith("www."):
            domain = domain[4:]
        if domain:
            candidates.append(f"https://logo.clearbit.com/{domain}")

    for url in candidates:
        try:
            r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code != 200:
                continue
            content = r.content
            # Byte-size gate: real logos are almost always > 5 KB
            if len(content) < 5000:
                continue
            if _pil_ok:
                img = _PIL.open(BytesIO(content))
                w, h = img.size
                if w < 128 or h < 128:    # reject anything smaller than 128×128
                    continue
            else:
                # Pillow not available — use a stricter byte threshold as proxy
                if len(content) < 15000:
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
    inject_css()

    # ── Sidebar ────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(EDEN_LOGO, unsafe_allow_html=True)

        st.markdown("**Stock Search**")
        ticker = st.selectbox(
            "Search ticker",
            options=TICKER_LIST,
            index=TICKER_LIST.index("AAPL") if "AAPL" in TICKER_LIST else 0,
            label_visibility="collapsed",
            placeholder="Type to search (e.g. NVD → NVDA)...")

        st.markdown("---")
        st.markdown("**Analysis Horizon**")
        horizon = st.radio(
            "Horizon", ["30D Tactical", "1Y Strategic"],
            index=0, label_visibility="collapsed")

        st.markdown("**Moving Averages**")
        col1, col2 = st.columns(2)
        with col1:
            ma1 = st.number_input("MA 1", min_value=0, max_value=200, value=50, help="0 = hidden")
        with col2:
            ma2 = st.number_input("MA 2", min_value=0, max_value=200, value=200, help="0 = hidden")

        st.markdown("**Indicators**")
        selected_indicators = st.multiselect(
            "Indicators",
            options=ALL_INDS,
            default=[],
            label_visibility="collapsed",
            placeholder="Add indicators...")

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

    # ── Tabs (no Forecast) ──────────────────────────────────────────────────
    _video_enabled = _node_available()
    _tab_names = ["📈 Chart", "📋 Report", "🔎 Peers", "📰 News", "📊 Financials",
                  "📅 Earnings", "👔 Insiders"]
    if _video_enabled:
        _tab_names.append("🎬 Video")
    _tabs = st.tabs(_tab_names)
    tab_chart, tab_rep, tab_peers, tab_news, tab_fin, tab_earn, tab_ins = _tabs[:7]
    tab_slides = _tabs[7] if _video_enabled else None

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
                df_peers = build_peers(ticker, self_info=data["info"], extra_peers=extra_tuple)
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


if __name__ == "__main__":
    main()
