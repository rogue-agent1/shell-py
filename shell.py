import shlex
class Shell:
    def __init__(s): s.vars={};s.cmds={"echo":s._echo,"set":s._set,"env":s._env,"cat":s._cat,"wc":s._wc,"rev":s._rev,"upper":s._upper}
    def _echo(s,args,stdin=None): return" ".join(args)
    def _set(s,args,stdin=None):
        if len(args)>=2: s.vars[args[0]]=" ".join(args[1:])
        return""
    def _env(s,args,stdin=None): return"
".join(f"{k}={v}" for k,v in s.vars.items())
    def _cat(s,args,stdin=None): return stdin or""
    def _wc(s,args,stdin=None):
        t=stdin or"";lines=t.count("
")+(1 if t and not t.endswith("
") else 0)
        return f"{lines} {len(t.split())} {len(t)}"
    def _rev(s,args,stdin=None): return(stdin or" ".join(args))[::-1]
    def _upper(s,args,stdin=None): return(stdin or" ".join(args)).upper()
    def _expand(s,token):
        for k,v in s.vars.items(): token=token.replace(f"",v)
        return token
    def execute(s,line):
        pipes=line.split("|");result=None
        for cmd in pipes:
            parts=cmd.strip().split();parts=[s._expand(p) for p in parts]
            name=parts[0];args=parts[1:]
            if name in s.cmds: result=s.cmds[name](args,result)
            else: result=f"unknown command: {name}"
        return result
def demo():
    sh=Shell()
    for cmd in["set name World","echo Hello ","echo hello world | upper","echo one two three four | wc","echo stressed | rev"]:
        r=sh.execute(cmd);print(f"$ {cmd}");
        if r: print(f"  {r}")
if __name__=="__main__": demo()
