# Contributing to this project

We want to make contributing to this project as easy and transparent as
possible.
This guide aims to provide you with all the necessary information to
get started and become an active part developer.

This guidelines will help you:

1.  🚀 [**Configure your environment**](#1--configure-your-environment)
    After cloning the repository, and running the Docker service, you'll
    need to configure your Visual Studio Code (VSCode) development
    environment.
    This section guides you through these initial steps,
    ensuring you're ready to contribute.<br></br>

2.  ✅ [**Review our commit conventions**](#commit-conventions)
    Our project follows specific
    commit conventions to maintain a clear and understandable history of
    changes. Adhering to these guidelines ensures that your contributions
    can be easily reviewed and incorporated.

# 1. 🚀 Configure your environment

To ensure a standardized and efficient development process across our
Python projects, we use specific tools. These tools enhance the quality
of your code and allow you to focus more on the complex and interesting
aspects of development.

The tools that we use are:

- **[Pylint](https://pylint.readthedocs.io/en/stable/)
  ([PEP8](https://peps.python.org/pep-0008/) convention)**:
  Linting support. This tool identifies syntactical and stylistic issues
  in Python code, helping to prevent potential errors and encourage best
  practices.

- **[Black](https://black.readthedocs.io/en/stable/)** Formatter:
  Code formatting. Black automatically formats Python code, improving
  readability and consistency without affecting functionality.

- **[Isort](https://pycqa.github.io/isort/)**: Sorting imports.
  Isort sorts imports in Python files, promoting uniformity and
  readability, which facilitates quicker code reviews and development
  cycles.

Note: If you are not using VSCode, you still need to use these tools
in your development environment to ensure compatibility and consistency.

### 📦 Install VSCode extensions:

Our development environment leverages several VSCode extensions.

- **[Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)**
- **[Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)**
- **[Isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)**

#### ⚙️ Configure VSCode Workspace

Proper configuration of the VSCode workspace is crucial.
Edit the `settings.json` file within the `.vscode` folder at the
project's root directory to include the following settings:

- **Pylint configuration**:

```json
"python.formatting.provider": "none",
"pylint.args": [
        "--max-line-length=79",
        "--rcfile",
        "${workspaceFolder}/.pylintrc",
        "--enable=W0614",
        "--generate-members"
    ],
```

- **Black Formatter configuration**:

```json
    "black-formatter.args": [
        "--line-length",
        "79"
    ],
```

- **Isort configuration**:

```json
    "isort.args": [
        "--profile",
        "black"
    ]
```

- **Python Editor configuration 🐍**:

```json
"[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.rulers": [
            79,
            72
        ],
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        },
        "editor.formatOnType": true
    },
```

This setup ensures that your Python code adheres to our formatting
guidelines, including a maximum line length of 79 characters for code
and 72 for comments, and organizes imports according to the
specified rules.

After completing these configurations, your VSCode environment will be
fully prepared for development within your container.

🌟 Remember to follow our commit convention guidelines
for a smooth collaboration process.

## Commit conventions

Commit messages should be clear and follow a certain format.
We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) & [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit). We also use some emojis to make the commit messages more expressive.
Some of the emojis are borrowed from [Gitmoji](https://gitmoji.dev/).

### Commit message format

The commit messages have a specific format, which includes a header, and optional body, and footer.

```bash
<type>(<scope>): <subject>

<body>

<footer>
```

#### Header

**type**: it describes the kind of change that the commit is introducing.
The types included are:

- ✨ `feat` - **Feature:** A new feature
- 📚 `doc` - **Documentation:** Changes to documentation
- 🐛 `fix` - **Bug Fix:** A bug fix
- 🎉 `init` - **Initialization:** Initial commits or major releases
- 🔨 `refactor` - **Refactor:** Code changes that neither fix a bug
  nor add a feature
- 🎨 `style` - **Style:** Changes that do not affect the meaning
  (white-space, formatting, etc)
- 🧹 `clean` - **Clean:** Deprecated code that needs to be cleaned up
- 🧪 `test` - **Test:** Adding missing tests or correcting existing
  tests
- ⚡ `perf` - **Performance:** Code changes that improve performance
- 🚀 `release` - **Release:** Release / Version tags
- 🏗️ `build` - **Build:** Changes that affect the build system or
  external dependencies
- 📔 `notebook` - **Notebook:** Changes to a notebook
- 🔒 `sec` - **Security:** Fixing security vulnerabilities
- 💻 `ci` - **Continuous Integration:** Changes to our CI configuration
  files and scripts
- 📦️ `lfile` - **Large File:** Add, modify, or remove a large file
- 🍄 `update` - **Update:** Update a feature
- 🔀 `merge` - **Merge:** Changes during merge
- ⏪ `revert` - **Revert:** Revert to a previous commit

**scope**: This is optional and refers to the specific part of the
codebase
that the changes affect (e.g. train, validation, data).

**subject**: This is a short description of the change. Use imperative,
present tense: "change" not "changed" nor "changes".

#### Body

The body is used to explain the waht and why of the commit, as opposed
to the how. It should provide a meaningful context and motivation for
the changes and can be as detailed as necessary.

#### Footer

The footer is used to reference Github (Gitlab) issues, pull requests,
or breaking changes. For instance, Closes #123, Fixes #456.

### Example

```bash
✨ feat(train): Add train model

Add a new training script for training a model on a new dataset

Closes #123
```

## Docstrings

For python docstrings, we adhere to the
[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
This includes conventions for writing clear, understandable code and
comprehensive docstrings.
Please ensure your code follows these guidelines.

Here is an example.

```python

def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all
        keys will be returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument
        is missing from the dictionary, then that row was not found in
        the table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """

```
