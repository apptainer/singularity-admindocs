def variableReplace(app, docname, source):
    """
    Takes the source on rst and replaces all the needed variables declared on
    variable_replacements structure
    """
    result = source[0]
    for key in app.config.variable_replacements:
        result = result.replace(key, app.config.variable_replacements[key])
    source[0] = result


# Add the needed variables to be replaced either on code or on text on the next
# dictionary structure.
variable_replacements = {
    # This is used in install instructions, so should be a full version
    "{InstallationVersion}" : "3.8.5",
    "\{userdocs\}" : "https://singularity.hpcng.org/user-docs/3.8",
    # The versions in the published guide URLs are for major.minor only
    "{adminversion}": "3.8",
    "{userversion}": "3.8",
    # The 'Singularity' noun is now a replacement so we can have
    # {Singularity}  rather than bare 'Singularity'... and HPCng can
    # replace to SingularityPRO so that it is clearer where docs
    # diverge a bit from Singularity<->SingularityPRO due to long-term backports etc.
    "{Singularity}": "Singularity",
    # Version of Go to be used in install instructions
    "{GoVersion}": "1.17.1"
}


def setup(app):
    app.add_config_value('variable_replacements', {}, True)
    app.connect('source-read', variableReplace)
    app.add_css_file('custom.css')
