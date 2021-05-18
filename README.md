# Discord-bot documentation

Repository which will the documentation for the bot, as a static webpage in the `/docs` directory and served by GitHub Pages.

# Building docs

Need sphinx installed: `pip3 install sphinx`
Need custom theme installed `pip3 install sphinx_pdj_theme`

May need graphviz installed in future iterations: [Graphviz](https://graphviz.org/)

Sphinx will need all the python files from the head branch to autogenerate files. Where it looks for autodocumented files is defined at the head of `sphinx-documentation/source/conf.py`

Run `make.bat html` in `sphinx-documentation/source`

Copy `sphinx-documentation/build` to `docs`

# Editing docs

Doc build files are located in `sphinx-documentation/source`

Output files are in `sphinx-documentation/build`

Docs are restructured text (rst). Info available here:

Sphinx documentation available here: [Sphinx](https://www.sphinx-doc.org/en/master/index.html)

Graphviz documentation available here.

# Documenting your code

Code can be documented by placing docstrings after the definition of a function, member, or class.

e.g, for a class 
```
class MyClass:
"""
This is a docstring.

This is what the class does.
"""
    def init(self, a_number):
	"""
	This is the init of the class.
	
	:param a_number: Number for class creation
	:type a_number: int
	"""
        self.my_number = a_number * 2
        """
        working number of class
		
        :type: int 
        """
		
    def get_modified(self, a_param):
	"""
	Gets a number modified based on class attributes.
	
	:param a_param: input num 
	:type a_param: int 
	:returns: The parameter multiplied by self.my_number 
	:rtype: int
	"""
        return a_param * self.my_number
```
	