import httpx
from fastmcp import FastMCP

mcp = FastMCP("KOSIS_Cloud_MCP")
API_KEY = "OGYxZjE1NDk1ODc2NjUwN2I5MWRiMTVkY2I4ZGMzNjY="
BASE_URL = "https://kosis.kr/openapi"

@mcp.tool()
async def search_kosis_stats(
    search_nm: str,
    start_count: int = 1,
    result_count: int = 10
) -> str:
    """
    국가통계포털(KOSIS)에서 키워드로 통계표 목록(기관ID, 통계표ID 등)을 검색합니다.
    - search_nm: 검색할 통계 키워드 (예: '강남구 인구', '범죄발생', '1인가구')
    """
    url = f"{BASE_URL}/statisticsSearch.do"
    params = {
        "method": "getList",
        "apiKey": API_KEY,
        "searchNm": search_nm,
        "startCount": str(start_count),
        "resultCount": str(result_count),
        "format": "json",
        "jsonVD": "Y"
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url, params=params)
        return response.text

@mcp.tool()
async def get_kosis_data(
    org_id: str,
    tbl_id: str,
    prd_se: str = "Y",
    new_est_prd_cnt: int = 3,
    obj_l1: str = "ALL",
    itm_id: str = "ALL"
) -> str:
    """
    국가통계포털(KOSIS)의 특정 통계표(orgId, tblId)에서 실제 통계 수치를 조회합니다.
    - org_id: 기관 ID (예: 통계청 '101', 서울시 '201')
    - tbl_id: 통계표 ID (search_kosis_stats로 조회한 TBL_ID)
    - prd_se: 수록주기 ('Y': 년, 'Q': 분기, 'M': 월)
    - new_est_prd_cnt: 최근 시점 개수 (기본 최근 3개년/분기)
    """
    url = f"{BASE_URL}/Param/statisticsParameterData.do"
    params = {
        "method": "getList",
        "apiKey": API_KEY,
        "orgId": org_id,
        "tblId": tbl_id,
        "prdSe": prd_se,
        "newEstPrdCnt": str(new_est_prd_cnt),
        "objL1": obj_l1,
        "itmId": itm_id,
        "format": "json",
        "jsonVD": "Y"
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url, params=params)
        return response.text
