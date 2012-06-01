from distutils.core import setup, Extension

keycode = Extension('keycode',
                    sources = ['keycode.c', 'keycodepy.c'],
                    extra_link_args = ['-framework', 'CoreFoundation',
                                       '-framework', 'ApplicationServices',
                                       '-framework', 'Carbon']
    )

setup(name = 'keycode',
      version = '1.0',
      description = 'Translate to and from keycodes',
      ext_modules = [keycode]
    )
