# Pybundy

## A simple lightweight front end package bundler written in python


Why python? It's what made sense to me at the time and it seemed like it would be a fun project. I was getting frustrated with many of the bundlers I was working with as I just needed something simple, so I started working on this which became much more complicated, but has also been a lot of fun.

## Dependencies
[css-html-js-minify](https://pypi.org/project/css-html-js-minify/)
[colorama](https://pypi.org/project/colorama/)

## Configuration file: pybundy.config.json

```
{
	"pybundy":{
		"modules":[
			"bootstrap",
			"jquery"
		],
		"js":{
			"path": "./app/js/",
			"output": "./public/js/script.js",
			"files": [
				"file1.js",
				"file2.js"
			],
			"force": [
				"./node_modules/popper.js/dist/popper.min.js"
			]
		},
		"css":{
			"path": "./app/css/",
			"output": "./public/css/styles.css",
			"files": [
				"file1.css",
				"file2.css"
			]
		}
	}
}
```

modules: List of node modules for pybundy to try and find. Looks in dist folder for minified files

path: Path to directory where files are stored that you would like bundled.

output: The file you would like all of your files bundled into

files: List of files to look for in path for bundling

force: Forces file in provided path into bundle



## Downloading Instructions

1. Clone the repo
2. Run npm install
3. Run python pybundy.py
