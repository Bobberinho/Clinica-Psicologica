export function login(username, password) {
    console.log(`Attempted login with username=${username} password=${password}`)
}

export async function api_get(path, params, method = "GET", payload={}) {
    let response
    console.log(`GETTING http://127.0.0.1:8000${path}?${params}...`)
    console.log(localStorage.getItem("token"))
    try {
        if (method == "GET")
            response = await fetch(`http://127.0.0.1:8000${path}?${params}`, {
                method: "GET",
                headers: {
                    "Token": localStorage.getItem("token")
                },
            })
        else if (method == "POST" && payload == {})
            response = await fetch(`http://127.0.0.1:8000${path}`, {
                method: "POST",
                headers: {
                    "Token": localStorage.getItem("token"),
                    "Content-Type": "application/json"
                },
            })
        else if (method == "POST")
            response = await fetch(`http://127.0.0.1:8000${path}?${params}`, {
                method: "POST",
                headers: {
                    "Token": localStorage.getItem("token"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload),
            })
    }
    finally {
        if (response !== undefined) {
            if (!response.ok) {
                const json = await response.json()
                let message = `${response.status}. `
                message += typeof json["detail"] !== 'undefined' ? json["detail"] : `${response.statusText}.`
                throw new Error(message)
            }
            return response.json() 
        }
    }
}

export async function api_login(email, password) {
    const params = new URLSearchParams()
    params.append("email", email)
    params.append("password", await hash(password))
    const token = await api_get("/login", params, "POST")
    localStorage.setItem("token", token.token)
    localStorage.setItem("token_type", token.type)
    console.log(localStorage.getItem("token"), localStorage.getItem("token_type"))
}
export async function api_logout() {
    console.log("LOGOUT")
    localStorage.setItem("token", "")
    localStorage.setItem("token_type", "")
    window.location.href = "/"
}

export async function hash(text) {
    let hashBuffer = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text))
    return Array.from(new Uint8Array(hashBuffer)).map((b) => b.toString(16).padStart(2, "0")).join("")
}

export function sort(arr, property) {
    return arr.sort((a, b) => a[property] > b[property] ? 1 : a[property] < b[property] ? -1 : 0)
}