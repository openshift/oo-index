# oo-index

This package is a general-purpose stand-alone [index](http://app-shifter.rhcloud.com) of [quickstarts](https://www.openshift.com/developers/extend) and [cartridges](https://www.openshift.com/developers/technologies/) for the [OpenShift hosting platform](http://openshift.github.io). 

This repository contains two major components: 

1. A basic user interface for browsing, searching, and launching open cloud compatible applications and services, built with help from [Python Flask](http://flask.pocoo.org/) and [Twitter bootstrap](http://angular-ui.github.io/bootstrap/).
2. Default content for [the index](http://app-shifter.rhcloud.com), which is loaded from the included [`quickstart.json` file](https://github.com/openshift/oo-index/blob/master/wsgi/static/quickstart.json).

## Host your own index

First you must generate you Github Client ID and Secret. Access you GitHub account settings page, select "Applications" and "Register a New Application".
Fill in the form with:

- Application Name: oo-index
- Homepage URL: https://index-$namespace.rhcloud.com
- Authorization callback URL: https://index-$namespace.rhcloud.com/login/callback

Press "Register Application" and take note of your credentials.

You can [spin up your own hosted instance of this project on OpenShift Online](https://openshift.redhat.com/app/console/application_types/custom?name=index&initial_git_url=https%3A%2F%2Fgithub.com/openshift/oo-index.git&cartridges[]=python-2.7) in a single click, or use the [rhc command line tool](https://www.openshift.com/get-started#cli) to help configure your local development environment and your OpenShift-hosted environment in a single step:

    rhc app create index python-2.7 GITHUB_CLIENT_ID=[github-client-id] GITHUB_CLIENT_SECRET=[github-client-secret] OO_INDEX_GITHUB_REPONAME=index OO_INDEX_GITHUB_USERNAME=[your-github-username]
    cd index
    git remote add upstream https://github.com/openshift/oo-index.git
    git pull -s recursive -X theirs upstream master
    git push

### Local Development

Simply start a local web server with your Application credentials:

    ./start-devel.sh GITHUB_CLIENT_ID GITHUB_CLIENT_SECRET

### Data Specification

Every entry in the `quickstart.json` file should include the following attributes:

    {
      "name": "Ghost",
      "default_app_name": 'ghost',
      "git_repo_url": "https://github.com/openshift-quickstart/openshift-ghost-quickstart.git",
      "cartridges": ["nodejs-0.10"],
      "website": "http://tryghost.org/",
      "version": "0.4",
      "env_variables": {"name1":"value1","name2":"value2"},
      "tags": ["node.js","ghost","blog"],
      "description": "Ghost is a free, open, simple blogging platform that's available to anyone who wants to use it"
    }

And should comply with the following data format guidelines:

* **name** - a human-readable name for this project, service, or application (required)
* **default_app_name** - a short name suggestion, for use in the hosted application url. No hyphens, spaces, or other special characters allowed (a-zA-Z0-9 only, optional) 
* **git_repo_url** - a URL that points to the project's source code (required)
* **cartridges** - an array of cartridge names (strings), starting with the base web runtime cartridge, and continuing with any additional cartridge-based dependencies (this content is required for all quickstart applications)
* **website** - URL pointing to a project homepage (optional)
* **demo_url** - A link to a live demo (optional)
* **version** - The release version for this project, usually a numeric string (optional)
* **env_variables** - a hash of name, value pairs that can be used to intialize the application (optional)
* **tags** - a csv list of relevant terms and labels (optional)
* **description** - a basic project description in plain text, with quotes escaped (optional)

Pull requests that don't meet this criteria will be rejected.

## Contribute via Pull Request

1. Fork the upstream project repository at: [https://github.com/openshift/oo-index](https://github.com/openshift/oo-index)
2. Add an openshift-compatible service or application to the project's `quickstarts.json` file, making sure to include each of the [required fields](#data-specification).
3. **Add** and **Commit** your changes locally:

        git add wsgi/static/quickstart.json
        git commit -m 'Adding a Wordpress application to the project index'
    
4. **Push** your changes to GitHub:

        git push
    
5. Then, [send us a Pull Request](https://github.com/openshift/oo-index/pulls) and we'll update [our hosted index](http://app-shifter.rhcloud.com)

#### Copyright

OpenShift Origin, except where otherwise noted, is released under the Apache License 2.0. See the LICENSE file located in each component directory. 



+[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/dmueller2001/oo-index/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
 +
