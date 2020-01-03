from pathlib import Path

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure


@task
def scm_init(ctx):
    """Init git repo (if required) and configure git flow.

    Raises:
        Failure: .gitignore does not exist

    Returns:
        None
    """
    if not Path('.gitignore').is_file():
        raise Failure('.gitignore does not exist')

    new_repo = not Path('.git').is_dir()

    if new_repo:
        uri_remote = 'git@github.com:{}/{}.git'.format(ctx.scm.repo_owner,
                                                       ctx.scm.repo_slug
                                                      )

        ctx.run('git init')
        ctx.run('git add .')
        ctx.run('git commit -m "new package from {} ({})"'.format(ctx.cc.name, ctx.cc.version))
        ctx.run('git remote add origin {}'.format(uri_remote))
        ctx.run('git tag -a "v_0.0.0" -m "cookiecutter ref"')

    ctx.run('git flow init -d')
    ctx.run('git flow config set versiontagprefix {}'.format(ctx.scm.version_tag_prefix))

    if new_repo:
        ctx.run('git push -u origin master')
        ctx.run('git push -u origin develop')
        ctx.run('git push --tags')


@task
def scm_push(ctx):
    """Push all branches and tags to origin."""

    for branch in ('develop', 'master'):
        ctx.run('git push origin {}'.format(branch))

    ctx.run('git push --tags')


@task
def scm_status(ctx):
    """Show status of remote branches."""
    ctx.run('git for-each-ref --format="%(refname:short) %(upstream:track)" refs/heads')


@task
def docs_clean(ctx):
    """Delete docs build dirs."""
    for pattern in ('docs/build', 'docs/stage'):
        ctx.run('rm -rf {}'.format(pattern))


@task(docs_clean)
def docs_build(ctx):
    """Build sphinx docs."""
    for dir_ in ('docs/build', 'docs/stage'):
        ctx.run('mkdir {}'.format(dir_))

    ctx.run('cp -r docs/source/* docs/stage')
    ctx.run('sphinx-apidoc -o docs/stage {}'.format(ctx.pkg.name))
    ctx.run('sphinx-build -b html docs/stage docs/build')


@task(help={'name': 'Type of release: Major, Minor, or Hotfix'})
def bump_version(ctx, name):
    """Bump version: major, minor, hotfix."""
    name = name if name != 'hotfix' else 'patch'
    ctx.run('bump2version {}'.format(name))


@task
def clean(ctx):
    """Clean Python bytecode."""
    ctx.run('find . | grep __pycache__ | xargs rm -rf')
    ctx.run('find . | grep .pytest_cache | xargs rm -rf')


@task(clean,docs_clean)
def cleaner(ctx):
    """Clean build artifacts."""
    patterns = ('build',
                'dist',
                '*.egg-info',
                'reports'
                )

    for pattern in patterns:
        ctx.run('rm -rf {}'.format(pattern))


@task(cleaner)
def cleanest(ctx):
    """Clean tox virtual environments."""
    ctx.run('rm -rf .tox')


@task(cleaner)
def test(ctx):
    """Run tests."""
    ctx.run('tox --parallel 4')


@task
def lint(ctx):
    """Run linters."""
    ctx.run('tox -e lint')


@task
def publish(ctx):
    """Publish package using twine."""
    uri = ctx['pub']['uri_master']

    env = {
        'TWINE_REPOSITORY_URL': uri,
        'TWINE_USERNAME': ctx['secrets']['pub'][uri]['user_name'],
        'TWINE_PASSWORD': ctx['secrets']['pub'][uri]['password']
        }

    ctx.run('twine upload --verbose dist/*', env=env)


@task()
def reports(ctx):
    """Generate reports."""
    ctx.run('tox -e report')


@task(test,lint,reports)
def build(ctx):
    """Build sdist and wheel."""
    ctx.run('python3 setup.py build sdist bdist_wheel')


@task(test,lint)
def test_merge(ctx):
    """Run tox tests and linters before merging."""
    pass


@task
def test_accept(ctx):
    """Run acceptance tests."""
    ctx.run('tox -e accept')

@task
def make_migrations(ctx):
    """Make Django db migrations."""
    ctx.run('mkdir -p media_hoard/data/migrations/')

    from django.conf import settings
    from django.core.management import execute_from_command_line

    argv = ['manage.py', 'makemigrations']

    settings.configure(
        INSTALLED_APPS = ('media_hoard.data',)
        )

    execute_from_command_line(argv)


docs = Collection()
docs.add_task(docs_clean, name="clean")
docs.add_task(docs_build, name="build")

scm = Collection()
scm.add_task(scm_init, name="init")
scm.add_task(scm_push, name="push")
scm.add_task(scm_status, name="status")

ns = Collection(bump_version, build, clean, cleaner, cleanest, lint, publish, reports,
                test, test_merge, test_accept, make_migrations)
ns.add_collection(docs, name="docs")
ns.add_collection(scm, name="scm")
