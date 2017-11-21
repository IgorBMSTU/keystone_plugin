
return {
    bool = function (a)
        if type(a) == "string" then
            return a == "true"
        else
            return a
        end
    end,
    default_domain = function(dao_factory)
        local domain, err = dao_factory.project:find_all({name = 'default_domain'})
        if not err and next(domain) then return domain[1]['id'] end
        return nil
    end,
    handle_dao_error = function(resp, err, func)
        if not resp.errors then
            resp.errors = {num = 0 }
        end
        resp.errors.num = 1 + resp.errors.num
        resp.errors[resp.errors.num] = {error = err, func = func }
    end,
    time_to_string = function(timestamp)
        return timestamp and os.date("%Y-%m-%dT%X.000000Z", timestamp) or "null"
    end,
    string_to_time = function(s)
        local format ="(%d+)-(%d+)-(%d+)T(%d+):(%d+):(%d+).(%d+)"
        local time = {}
        time.day, time.month, time.year, time.hour, time.min, time.sec, time.zone=s:match(format)
        return os.time(time)
    end,
    parse_json = function(file_name)
        local storage = {}
        local file, err = io.open(file_name, "r")
        if not file or err then
            return err
        end

        while true do
            local t = file:read("*line")
            if not t then
                break
            end
            local a, b = t:match('\"(.*)\":%s\"(.*)\"')
            if a then
                storage[a] = b
            end

        end
        file:close()

        return nil, storage
    end

}
