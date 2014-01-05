hcpsdkupdater
=============
Tool to update SAP Hana Cloud SDK

This script is useful if you want to automate the installation or the upgrade of the #saphcp SDK.

Usage:

Execute this command in a shell:

python updater.sh [OPTIONS]

AVAILABLE OPTIONS:

-l or --list-availabes: list all the available online saphcp sdk versions of the.

-s or --set-sdk-type: Set the sdk version type to use (1.x Web or 2.x Web Profile). 

-u or --update-to-version <<version>>: Update sdk to specified version. Default update to 'latest' version 2

