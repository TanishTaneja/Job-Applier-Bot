from datetime import datetime
from typing import Dict, Any, List, Tuple
from scheduler.config.graphql import make_graphql_request

def get_search_jobs_query() -> Tuple[str, Dict[str, Any]]:
    query = """
    query searchJobCardsByLocation($searchJobRequest: SearchJobRequest!) {
      searchJobCardsByLocation(searchJobRequest: $searchJobRequest) {
        nextToken
        jobCards {
          jobId
          language
          dataSource
          requisitionType
          jobTitle
          jobType
          employmentType
          city
          state
          postalCode
          locationName
          totalPayRateMin
          totalPayRateMax
          tagLine
          bannerText
          image
          jobPreviewVideo
          distance
          featuredJob
          bonusJob
          bonusPay
          scheduleCount
          currencyCode
          geoClusterDescription
          surgePay
          jobTypeL10N
          employmentTypeL10N
          bonusPayL10N
          surgePayL10N
          totalPayRateMinL10N
          totalPayRateMaxL10N
          distanceL10N
          monthlyBasePayMin
          monthlyBasePayMinL10N
          monthlyBasePayMax
          monthlyBasePayMaxL10N
          jobContainerJobMetaL1
          virtualLocation
          poolingEnabled
          payFrequency
          __typename
        }
        __typename
      }
    }
    """

    variables = {
        "searchJobRequest": {
            "locale": "en-US",
            "country": "United States",
            "dateFilters": [
                {
                    "key": "firstDayOnSite",
                    "range": {
                        "startDate": datetime.now().strftime("%Y-%m-%d")
                    },
                }
            ],
            "sorters": [
                {
                    "fieldName": "totalPayRateMax",
                    "ascending": "false",
                }
            ],
            "pageSize": 100,
        }
    }

    return query, variables


def get_search_jobs() -> List[Dict[str, Any]]:
    query, variables = get_search_jobs_query()
    response_data = make_graphql_request(query, variables)

    if not response_data:
        return []

    data = response_data.get("data")
    if not isinstance(data, dict):
        return []

    search_jobs = data.get("searchJobCardsByLocation")
    if not isinstance(search_jobs, dict):
        return []

    job_cards = search_jobs.get("jobCards")
    if not isinstance(job_cards, list):
        return []

    return job_cards