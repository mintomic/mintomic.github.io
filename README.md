This is the [Jekyll](http://jekyllrb.com/) source repository for the [Mintomic documentation](http://mintomic.github.io/). It features a table of contents. To keep the table of contents up-to-date, you need to follow some rules.

## How to Maintain the Table of Contents

All of the Markdown pages in this repository form a linked list, starting with the [root `index.md` page](https://github.com/mintomic/mintomic.github.io/blob/master/index.md). Each page has a link to the next page stored in the `next` variable in its YAML front matter section. It's a full path relative to the root. If you insert, delete or rename pages, you must update these `next` links by hand.

Once all the `next` links are up-to-date, run the Python script found at `_scripts/link_pages.py`. It will update the `prev`, `prev_title`, `up`, `up_title`, and `next_title` variables in each page's YAML front matter. It also generates `_includes/toc.html`. All these stuff gets referenced in the Liquid templates of `_layouts/default.html` when Jekyll generates the static pages for the site.
