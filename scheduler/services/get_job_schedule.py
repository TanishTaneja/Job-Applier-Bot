from datetime import datetime
from typing import List, Any
from scheduler.config.graphql import make_graphql_request


def get_job_schedule_query(job_id: str) -> tuple[str, dict[str, Any]]:
    query = """
    query searchScheduleCards($searchScheduleRequest: SearchScheduleRequest!) {
        searchScheduleCards(searchScheduleRequest: $searchScheduleRequest) {
            nextToken
            scheduleCards {
                hireStartDate
                address
                basePay
                bonusSchedule
                city
                currencyCode
                dataSource
                distance
                employmentType
                externalJobTitle
                featuredSchedule
                firstDayOnSite
                hoursPerWeek
                image
                jobId
                jobPreviewVideo
                language
                postalCode
                priorityRank
                scheduleBannerText
                scheduleId
                scheduleText
                scheduleType
                signOnBonus
                state
                surgePay
                tagLine
                geoClusterId
                geoClusterName
                siteId
                scheduleBusinessCategory
                totalPayRate
                financeWeekStartDate
                laborDemandAvailableCount
                scheduleBusinessCategoryL10N
                firstDayOnSiteL10N
                financeWeekStartDateL10N
                scheduleTypeL10N
                employmentTypeL10N
                basePayL10N
                signOnBonusL10N
                totalPayRateL10N
                distanceL10N
                requiredLanguage
                monthlyBasePay
                monthlyBasePayL10N
                vendorKamName
                vendorId
                vendorName
                kamPhone
                kamCorrespondenceEmail
                kamStreet
                kamCity
                kamDistrict
                kamState
                kamCountry
                kamPostalCode
                payFrequency
                __typename
            }
            __typename
        }
    }
    """

    variables = {
        "searchScheduleRequest": {
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
            "pageSize": 1000,
            "jobId": job_id,
        }
    }

    return query, variables


def get_job_schedule(job_id: str) -> List[dict]:
    query, variables = get_job_schedule_query(job_id)
    response_data = make_graphql_request(query, variables)

    if not response_data:
        return []

    data = response_data.get("data")
    if not isinstance(data, dict):
        return []

    search_schedules = data.get("searchScheduleCards")
    if not isinstance(search_schedules, dict):
        return []

    schedule_cards = search_schedules.get("scheduleCards")
    if not isinstance(schedule_cards, list):
        return []

    return schedule_cards