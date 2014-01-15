# oo-index

This package is a general-purpose stand-alone [index](http://app-shifter.rhcloud.com) of [quickstarts](https://www.openshift.com/developers/extend) and [cartridges](https://www.openshift.com/developers/technologies/) for the [OpenShift hosting platform](http://openshift.github.io). 

This repository contains two major components: 

1. A basic user interface for browsing, searching, and launching open cloud compatible applications and services, built with help from [Angular-js and Twitter bootstrap](http://angular-ui.github.io/bootstrap/).
2. Default content for [the index](http://app-shifter.rhcloud.com), which is loaded from the included [`quickstart.json` file](https://github.com/openshift/oo-index/blob/master/quickstart.json).

## Host your own index

You can [spin up your own hosted instance of this project on OpenShift Online](https://openshift.redhat.com/app/console/application_types/custom?name=index&initial_git_url=https%3A%2F%2Fgithub.com/openshift/oo-index.git&cartridges[]=nodejs-0.10) in a single click, or use the [rhc cpmmand line tool](https://www.openshift.com/get-started#cli) to help configure your local development environment and your OpenShift-hosted environment in a single step:

    rhc app create index nodejs-0.10 --from-code=https://github.com/openshift/oo-index.git

### Data Specification

Every entry in the `quickstatart.json` file should include the following attributes:

    {
     "name":"Ghost",
      "website":"http://tryghost.org/",
      "version":"0.1",
      "initial_git_url":"https://github.com/openshift-quickstart/openshift-ghost-quickstart.git",
      "cartridges":["nodejs-0.10"],
      "env_variables":[{"name":"value"},{"name":"value"}],
      "tags":["node.js","ghost","blog"],
      "summary":"Ghost is a free, open, simple blogging platform that's available to anyone who wants to use it"
    }</javascript>

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
