# oo-index

This package is a general-purpose stand-alone [index](http://app-shifter.rhcloud.com) of [quickstarts](https://www.openshift.com/developers/extend) and [cartridges](https://www.openshift.com/developers/technologies/) for the [OpenShift hosting platform](http://openshift.github.io). 

This repository contains two major components: 

1. A basic user interface for browsing, searching, and launching open cloud compatible applications and services, built with help from [Angular-js and Twitter bootstrap](http://angular-ui.github.io/bootstrap/).
2. Default content for [the index](http://app-shifter.rhcloud.com), which is loaded from the included [`quickstart.json` file](https://github.com/openshift/oo-index/blob/master/quickstart.json).

## Host your own index

You can [spin up your own hosted instance of this project on OpenShift Online](https://openshift.redhat.com/app/console/application_types/custom?name=index&initial_git_url=https%3A%2F%2Fgithub.com/openshift/oo-index.git&cartridges[]=nodejs-0.10) in a single click, or use the [rhc command line tool](https://www.openshift.com/get-started#cli) to help configure your local development environment and your OpenShift-hosted environment in a single step:

    rhc app create index nodejs-0.10 --from-code=https://github.com/openshift/oo-index.git

### Local Development

First, make sure that your npm dependencies are available:

    npm install
    
Then, start a local web server:
    
    npm start

The project source can be re-bundled by running:

    npm run build
    
Additional scripts for assisting with development work are [defined in the project's `package.json` file](https://github.com/openshift/oo-index/blob/master/package.json#L23).


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
* **cartridges** - csv list of strings, starting with the base cartridge type, and continuing with any additional cartridge-based dependencies (required for quickstart applications)
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

        git add quickstart.json
        git commit -m 'Adding a Wordpress application to the project index'
    
4. **Push** your changes to GitHub:

        git push
    
5. Then, [send us a Pull Request](https://github.com/openshift/oo-index/pulls) and we'll update [our hosted index](http://app-shifter.rhcloud.com)

#### Copyright

OpenShift Origin, except where otherwise noted, is released under the Apache License 2.0. See the LICENSE file located in each component directory. 



+[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/dmueller2001/oo-index/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
 +
