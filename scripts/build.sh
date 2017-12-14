# A script that builds stylesheets and JavaScript sources.

#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build stylesheets.
echo -e "\e[1;45mBuilding stylesheets...\e[0m"
pushd $DIR/../www/css
npm run gulp package-dev
popd

# Build the frontend code.
echo -e "\e[1;45mBuilding JavaScript sources...\e[0m"
pushd $DIR/../www/js
npm run gulp package-dev
popd
