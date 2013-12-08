infect
======

dotfiles distribution management

# RDD note

This awesome project is developed according to Readme-Driven-Development
principle and this readme is used to capture all the ideas we have for the
implementation.

# Workflow

## Create your dotfiles

  $ pip install infect
  $ infect init --user johndoe
  $ infect list-apps
  $ infect list-configs vim
  $ infect clone-config tonylazarew/dotvim --to johndoe/dotvim
  $ infect upload

`upload` step uploads tarball and pushes changes to all relevant github
repositories (or maybe only tarball?)

## Infect random hosts

  $ curl http://johndoe.infect.se | python

## Edit your dotfiles and upload

  $ infect gitify ~/sources/dotfiles

This will make `~/sources/dotfiles` as a convenience symlink to your actual
infect dotfiles (usually stored in `~/.local/share/infect`) and will transform
them into git repositories so that you can commit back to your original github
repos.

## Share your config with others

By default all configs for apps will be hidden from `list-config` command. To
share your configuration with others, do:

  $ infect share vim

This will tag your current repo state with a `shared` tag and this snapshot
will be available for others to use. Once you've modified your config, run
`share vim` again to share the new version.

## Create a config

  $ infect create-config --app tmux --to johndoe/dottmux

This will create a skeleton repo for your tmux configuration and will submit it
to your `dottmux` GitHub repo. Note, that this repo must already exist on
GitHub.
