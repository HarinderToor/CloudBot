from cloudbot import hook


@hook.command('offtopic')
def offtopic(text, nick):
    if not text:
        return
    if text.startswith('#'):
        hash_text = 'reddit-tennis-' + text
    else:
        hash_text = '#reddit-tennis-' + text
    return('Please keep off-topic chat to a minimum, or take it to ' + hash_text)
