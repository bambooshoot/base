import os

# Set Environ Path
def setEnviron(key, path):
    envData = os.environ.get(key)
    if envData:
        if os.path.exists(path):
            if not path in envData:
                os.environ[key] += '%s%s' % (os.pathsep, path)
                traceMessage = 'Set Environ [ %s ] : %s' % (key, path)
                core.mel.trace(traceMessage)
            elif path in envData:
                traceMessage = 'Exists - Environ [ %s ] : %s' % (key, path)
                core.mel.trace(traceMessage)
        if not os.path.exists(path):
            traceMessage = 'Non - Exists Path [ %s ] : %s' % (key, path)
            core.mel.trace(traceMessage)
    if not envData:
        os.environ[key] = path
        traceMessage = 'Set Environ [ %s ] : %s' % (key, path)
        core.mel.trace(traceMessage)
