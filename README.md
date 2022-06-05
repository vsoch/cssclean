# CSS Clean!

[![PyPI version](https://badge.fury.io/py/cssclean.svg)](https://badge.fury.io/py/cssclean)

This is a library for cleaning up css based on styles that are actually used in html files.
Although there are [libraries that use npm](https://www.keycdn.com/blog/remove-unused-css)
I am not a fan so I wanted something in Python.

## Approach

We take a conservative approach to filtering, meaning:

 - for any style block, one matching class or identifier is sufficient for inclusion
 - multiple levels selectors are not combined (e.g., using "button" is sufficient to add `.button. red`.

Of course this could be improved upon but we would need more careful token parsing!
Please [open an issue](https://github.com/vsoch/cssclean/issues) if you are interested. 

## Usage

### Install

First, clone and install.

```bash
$ git clone https://github.com/vsoch/cssclean
$ cd cssclean
$ pip install -e .
```

or install from pip.

```bash
$ pip install cssclean
```

And then try running an example! 

### Clean Directory

Below we ask cssclean to automatically detect files (css and html) under the same test directory:

```bash
$ cssclean clean --css cssclean/tests/testdata/1 --html cssclean/tests/testdata/1
Sheet style.css has 124 rules.
Sheet style.css filtered down to 43 rules.
1 files written:
  style.css => /home/vanessa/Desktop/Code/unused-css/cssclean/tests/testdata/1/style.clean.css
```

As you can see, by default, it will write the updated css files alongside the old files but with .clean added.
Note that you can provide individual files, one at a time too, for both of ``--css``
and ``--html``.

```bash
$ cssclean clean --css cssclean/tests/testdata/1 --html cssclean/tests/testdata/1/home.html --html cssclean/tests/testdata/1/table.html
```

### Dry Run

You can also do a dry run to print the filtered style to the screen:

```bash
$ cssclean clean --css cssclean/tests/testdata/1 --html cssclean/tests/testdata/1 --dry-run
...
.card.yellow {
  background-color: var(--color-yellow);
}
tr {
  background-color: white;
}
```

### Minify

And you can ask for the same preview, but minified:

```bash
$ cssclean clean --css cssclean/tests/testdata/1 --html cssclean/tests/testdata/1 --dry-run --minify
```

Or a non-preview minified:

```bash
$ cssclean clean --css cssclean/tests/testdata/1 --html cssclean/tests/testdata/1 --outdir ./out --minify
```
```bash
Sheet style.css has 124 rules.
Sheet style.css filtered down to 43 rules.
1 files written:
  style.css => ./out/style.clean.min.css
```

Note that "min" is added to the saved filename.

### Output Directory

You can also ask for a custom output directory:

```bash
$ mkdir out
$ cssclean clean --css cssclean/tests/testdata/1 --html cssclean/tests/testdata/1 --outdir ./out
```
```bash
Sheet style.css has 124 rules.
Sheet style.css filtered down to 43 rules.
1 files written:
  style.css => ./out/style.clean.css
```



## Contributors

We use the [all-contributors](https://github.com/all-contributors/all-contributors) 
tool to generate a contributors graphic below.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://vsoch.github.io"><img src="https://avatars.githubusercontent.com/u/814322?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Vanessasaurus</b></sub></a><br /><a href="https://github.com/vsoch/cssclean/commits?author=vsoch" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## TODO

 - add tests for different cases
 - create GitHub actions - one to actually clean and one to detect (fail if unused)
 - automated release
 - some kind of summary command that shows used/unused styles, or the count
 - contributors workflow
 
## License

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
