def show_command(cmd, c_args=None):
    s = "{cmd} {c_args}".format(
        cmd=cmd,
        c_args=c_args,
        )
    print(s)

def show_config(alias, values):
    s = "{username}@{alias}".format(
        alias=alias,
        username=values['auth']['HTTPBasicAuth']['username'],
        )
    print(s)

def show_content(c):
    print(c)

def show_server_error(e):
    s = """Oops! seems to be having a problem. {}""".format(e.message)
    print(s)
