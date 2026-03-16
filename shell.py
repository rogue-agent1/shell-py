class Shell:
    def __init__(s): s.vars={};s.cmds={"echo":s._echo,"set":s._set,"env":s._env,"wc":s._wc,"rev":s._rev,"upper":s._upper}
    def _echo(s,args,stdin=None): return " ".join(args)
    def _set(s,args,stdin=None):
        if len(args)>=2: s.vars[args[0]]=" ".join(args[1:])
        return ""
    def _env(s,args,stdin=None): return "\n".join(k+"="+v for k,v in s.vars.items())
    def _wc(s,args,stdin=None):
        t=stdin or "";lines=t.count("\n")+(1 if t and not t.endswith("\n") else 0)
        return str(lines)+" "+str(len(t.split()))+" "+str(len(t))
    def _rev(s,args,stdin=None): return (stdin or " ".join(args))[::-1]
    def _upper(s,args,stdin=None): return (stdin or " ".join(args)).upper()
    def _expand(s,token):
        for k,v in s.vars.items(): token=token.replace("$"+k,v)
        return token
    def execute(s,line):
        pipes=line.split("|");result=None
        for cmd in pipes:
            parts=cmd.strip().split();parts=[s._expand(p) for p in parts]
            name=parts[0];args=parts[1:]
            if name in s.cmds: result=s.cmds[name](args,result)
            else: result="unknown: "+name
        return result
def demo():
    sh=Shell()
    for cmd in["set name World","echo Hello $name","echo hello world | upper","echo one two three | wc","echo stressed | rev"]:
        r=sh.execute(cmd);print("$ "+cmd)
        if r: print("  "+r)
if __name__=="__main__": demo()
