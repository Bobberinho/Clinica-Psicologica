export function login(username, password) {
    console.log(`Attempted login with username=${username} password=${password}`)
}

export async function fetch(path) {
    const response = await fetch(`http://127.0.0.1:8000/${path}`)
    if (!response.ok) {
        if (response.status === 404) throw new Error('Not found')
        throw new Error('Server error')
    }
    return response
}