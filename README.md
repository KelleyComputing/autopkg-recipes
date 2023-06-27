# autopkg-recipes

Recipes used for AutoPkg software update automation.

## Use with SimpleMDM

When overriding a Munki recipe, it's necessary to specify the following dict keys in order to use the SimpleMDM Munki integration:

```
<key>MUNKI_REPO</key>
<string>""</string>
<key>MUNKI_REPO_PLUGIN</key>
<string>SimpleMDMRepo</string>
```
