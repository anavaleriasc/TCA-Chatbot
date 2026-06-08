export type AuthPayload = {
    email: string,
    password : string
}

export type User = {
    id: number,
    email: string,
}

export type AuthResponse = {
    access_token: string,
    token_type: string,
    user: User
   

}