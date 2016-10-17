
define([
    'base/js/namespace',
    'jquery',
    'base/js/utils',
    './common',
], function(IPython, $, utils, common) {
    "use strict";

    var NullView = {
        refresh: function() {}
    };

    var base_url = (IPython.notebook_list || IPython.notebook).base_url;

    var environments = {
        all:      [],
        selected: null,
        view:     NullView,

        load: function() {
            // Load the list via ajax to the /environments endpoint
            var that = this;
            var error_callback = common.MakeErrorCallback('Error', 'An error occurred while listing Conda environments.');

            function handle_response(envs, status, xhr) {
                var keep_selection = false;
                var default_env;

                that.all = envs;

                // Select the default environment as current
                $.each(envs, function(index, env) {
                    if(env.is_default) {
                        default_env = env;
                    }

                    if(that.selected && that.selected.name == env.name) {
                        // selected env still exists
                        keep_selection = true;
                    }
                });

                that.view.refresh(envs);

                if(! keep_selection) {
                    // Lost selected env, pick a different one
                    that.select(default_env);
                }
            }

            var settings = common.AjaxSettings({
                success: common.SuccessWrapper(handle_response, error_callback),
                error:   error_callback
            });

            var url = utils.url_join_encode(base_url, 'environments');
            return $.ajax(url, settings);
        },

        select: function(env) {
            this.selected = env;

            // refresh list of packages installed in the selected environment
            return installed.load();
        },

        create: function(name, type) {
            var error_callback = common.MakeErrorCallback('Error Creating Environment', 'An error occurred while creating "' + name + '"');

            function create_success() {
                // Refresh list of environments since there is a new one
                environments.load();
            }
            return conda_env_action({ name: name }, 'create', create_success, error_callback, { type: type });
        },

        clone: function(env, new_name) {
            var error_callback = common.MakeErrorCallback('Error Cloning Environment', 'An error occurred while cloning "' + env.name + '"');

            function clone_success() {
                // Refresh list of environments since there is a new one
                environments.load();
            }
            return conda_env_action(env, 'clone', clone_success, error_callback, { name: new_name });
        },

        remove: function(env) {
            var error_callback = common.MakeErrorCallback('Error Removing Environment', 'An error occurred while removing "' + env.name + '"');

            function remove_success() {
                // Refresh list of environments since there is a new one
                environments.load();
            }
            return conda_env_action(env, 'delete', remove_success, error_callback);
        }
    };

    function conda_package_action(packages, action, on_success, on_error) {
        // Helper function to access the /environments/ENV/packages/ACTION endpoint

        var settings = common.AjaxSettings({
            data:    { packages: packages },
            type:    'POST',
            success: common.SuccessWrapper(on_success, on_error),
            error:   on_error
        });

        var url = utils.url_join_encode(base_url, 'environments', environments.selected.name, 'packages', action);
        return $.ajax(url, settings);
    }

    function conda_env_action(env, action, on_success, on_error, data) {
        // Helper function to access the /environments/ENV/ACTION endpoint

        // pre-condition names that may have come from nb_conda_kernels
        if(env.name === "Root"){
            env.name = "root";
        }

        var settings = common.AjaxSettings({
            data:    data || {},
            type:    'POST',
            success: common.SuccessWrapper(on_success, on_error),
            error:   on_error
        });

        var url = utils.url_join_encode(base_url, 'environments', env.name, action);
        return $.ajax(url, settings);
    }

    var available = {
        packages: [],
        view:     NullView,

        load: function() {
            // Load the package list via ajax to the /packages/available endpoint
            var that = this;

            function handle_response(packages, status, xhr) {
                if(xhr.status == 202) {
                    // "Accepted" - try back later on this async request
                    setTimeout(function() {
                        that.load();
                    }, 1000);
                }
                else {
                    $.each(packages, function(index, pkg) {
                        pkg.selected = false;
                    });

                    that.packages = packages;
                    that.view.refresh(that.packages);
                }
            }

            var error_callback = common.MakeErrorCallback('Error', 'An error occurred while retrieving package information.');

            var settings = common.AjaxSettings({
                success : common.SuccessWrapper(handle_response, error_callback),
                error : error_callback
            });

            var url = utils.url_path_join(base_url, 'packages', 'available');
            return $.ajax(url, settings);
        },

        get_selection: function() {
            return this.packages.filter(function(pkg) {
                return pkg.selected;
            });
        },

        select_none: function() {
            $.each(this.packages, function(index, pkg) {
                pkg.selected = false;
            });
        },

        get_selected_names: function() {
            return this.get_selection().map(function(pkg) {
                return pkg.name;
            });
        },

        conda_install: function() {
            var that = this;
            var packages = this.get_selected_names();

            if(packages.length == 0) {
                return;
            }

            var error_callback = common.MakeErrorCallback('Error Installing Packages', 'An error occurred while installing packages.');

            function install_success() {
                // Refresh list of packages installed in the current environment
                installed.load();
                that.select_none();
                that.view.refresh(that.packages);
            }
            return conda_package_action(packages, 'install', install_success, error_callback);
        }
    };


    var installed = {
        packages: [],
        by_name:  {},
        view:     NullView,

        load: function() {
            if(environments.selected !== null) {
                return this.conda_list(environments.selected.name);
            }
            else {
                // Need an environment in order to display installed packages.
                this.packages = [];
                this.by_name = {};
                this.view.refresh([]);
                return $.Deferred().resolve();
            }
        },

        get_selection: function() {
            return this.packages.filter(function(pkg) {
                return pkg.selected;
            });
        },

        get_selected_names: function() {
            return this.get_selection().map(function(pkg) {
                return pkg.name;
            });
        },

        conda_list: function(query) {
            // Load the package list via ajax to the /packages/search endpoint
            var that = this;

            function handle_response(packages, status, xhr) {
                var by_name = {};

                $.each(packages, function(index, pkg) {
                    pkg.selected = false;
                    pkg.available = '';
                    by_name[pkg.name] = pkg;
                });

                that.packages = packages;
                that.by_name  = by_name;
                that.view.refresh(that.packages);
            }

            var error_callback = common.MakeErrorCallback('Error', 'An error occurred while retrieving installed packages.');

            var settings = common.AjaxSettings({
                success: common.SuccessWrapper(handle_response, error_callback),
                error:   error_callback
            });

            var url = utils.url_join_encode(base_url, 'environments', query);
            return $.ajax(url, settings);
        },

        _update: function(dry_run, handler) {
            // Load the package list via ajax to the /environments/ENV/check endpoint
            var that = this;

            var packages = this.get_selected_names();

            if(packages.length == 0) {
                // If no packages are selected, update all
                packages = ['--all'];
            }

            var action;
            var msg;

            if(dry_run) {
                action = 'check';
                msg = 'An error occurred while checking for package updates.';
            }
            else {
                action = 'update';
                msg = 'An error occurred while updating packages.';
            }

            var error_callback = common.MakeErrorCallback('Error', msg);
            return conda_package_action(packages, action, handler, error_callback);
        },

        conda_check_updates: function() {
            var that = this;

            function handle_response(updates, status, xhr) {
                $.each(updates, function(index, pkg) {
                    var existing = that.by_name[pkg.name];

                    // See if there is an existing entry.
                    // Usually there will be, but an update
                    // might pull in a new package as a dependency.
                    if(existing) {
                        existing.available = pkg.version + '-' + pkg.build;
                    }
                });

                that.view.refresh(that.packages);
            }

            return this._update(true, handle_response);
        },

        conda_update: function() {
            var that = this;

            function handle_response(packages, status, xhr) {
                // Refresh list of packages to reflect changes
                that.load();
            }

            return this._update(false, handle_response);
        },

        conda_remove: function() {
            var that = this;
            var packages = this.get_selected_names();

            if(packages.length == 0) {
                return;
            }

            var error_callback = common.MakeErrorCallback('Error Removing Packages', 'An error occurred while removing packages.');

            function remove_success() {
                // Refresh list of packages installed in the current environment
                installed.load();
            }
            return conda_package_action(packages, 'remove', remove_success, error_callback);
        }
    };

    return {
        'base_url':     base_url,
        'environments': environments,
        'available':    available,
        'installed':    installed
    };
});
