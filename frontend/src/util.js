export function login(username, password) {
    console.log(`Attempted login with username=${username} password=${password}`)
}

export async function api_get(path, params) {
    try {
        const response = await fetch(`http://127.0.0.1:8000${path}?${params}`, {
            method: "GET",
            headers: {
                "Token": localStorage.getItem("token")
            }
        })
        if (!response.ok) {
            if (response.status === 404) throw new Error('Not found')
            throw new Error('Server error')
        }
        console.log(`GET http://127.0.0.1:8000${path}?${params}`)
        return response.json()
    }
    catch {
        return ""
    }
}
export async function api_post(path, params) {
    try {
        const response = await fetch(`http://127.0.0.1:8000${path}?${params}`, {
            method: "POST",
        })
        if (!response.ok) {
            if (response.status === 404) throw new Error('Not found')
            throw new Error('Server error')
        }
        console.log(`http://127.0.0.1:8000${path}?${params}`)
        return response.json()
    }
    catch {
        return ""
    }
}
export async function api_login(email, password) {
    const params = new URLSearchParams()
    params.append("email", email)
    params.append("password", await hash(password))
    const token = await api_post("/login", params)
    localStorage.setItem("token", token.token)
    localStorage.setItem("token_type", token.type)
    console.log(localStorage.getItem("token"), localStorage.getItem("token_type"))
}

export async function hash(text) {
    let hashBuffer = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text))
    return Array.from(new Uint8Array(hashBuffer)).map((b) => b.toString(16).padStart(2, "0")).join("")
}

export function sort(arr, property) {
    return arr.sort((a, b) => a[property] > b[property] ? 1 : a[property] < b[property] ? -1 : 0)
}