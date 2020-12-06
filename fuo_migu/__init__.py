# *-- coding: utf-8 --*
__alias__ = '咪咕音乐'
__feeluown_version__ = '3.6'
__version__ = '0.1.0'
__desc__ = __alias__
__identifier__ = 'migu'

from feeluown.app import App

from fuo_migu.provider import provider


def enable(app):
    app.library.register(provider)
    if app.mode & App.GuiMode:
        pm = app.pvd_uimgr.create_item(
            name=provider.identifier,
            text=__alias__,
            symbol='🎵️ ',
            desc='未实现',
        )
        app.pvd_uimgr.add_item(pm)


def disable(app: App):
    app.library.deregister(provider)
    if app.mode & App.GuiMode:
        app.providers.remove(provider.identifier)
