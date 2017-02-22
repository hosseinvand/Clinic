const API_ROOT = "https://asd-clinic.herokuapp.com/notebook/api/"

export function getFullUrl(endpoint) {
    const fullUrl = (endpoint.indexOf(API_ROOT) === -1) ? API_ROOT + endpoint : endpoint
    return fullUrl
}