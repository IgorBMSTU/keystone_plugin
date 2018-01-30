local responses = require "kong.tools.responses"
local utils = require "kong.tools.utils"
local kutils = require ("kong.plugins.keystone.utils")
local cjson = require "cjson"
local urandom = require ("randbytes")
local fernet = require ("resty.fernet")

local function validate_token(dao_factory, token_id, validate)
    responses.send_HTTP_BAD_REQUEST("Fernet Tokens can't be validated or revoked")
end

local function check_token(token, dao_factory, allow_expired, validate)
    -- token: { id }
    -- bool allow_expired:
    -- return token: { id, user_id }
    return token
end

local function generate_token(dao_factory, user, cached, scope_id)
    -- user: { id }
    -- bool cached
    -- return token: { id, expires, roles, issued_at }
    local token_str = [[gAAAAABWHXT73mGHg90PE6rmS-6aeYYvdErvO1RCWbDBrM5JV6L-eGEkz9cv8598DWWF5LZH5buzYM6PmUk3w9PHd4j6zs9L0_nvqZAGOrA4gLjhE10MLk00_Qy-IIPMQ6kxjsphYVLP1uBUNyh-s4hq76-KGNUqAcYgLyN8DtgoifDseSZKNl8]]
    local secret = 'MmcGs0_iRH-GybC41AcxdtgvgIi4kk3T94bAqoL7l-k='
    local payload = fernet:verify(secret, token_str, 0).payload
    local uu = utils.uuid()
    responses.send_HTTP_BAD_REQUEST({touuid(payload), uu})
--    responses.send_HTTP_BAD_REQUEST({urandom(16), uu, uu:byte(1, #uu)})

    local token = {}
    return token
end

local function get_token_info(token_id)
    -- return token: { user_id, scope_id, roles, issued_at, is_admin }
    local token = {}
    return token
end

return {
    generate = generate_token,
    validate = validate_token,
    check = check_token,
    get_info = get_token_info
}