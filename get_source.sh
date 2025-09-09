#!/bin/bash
set -e

VERSION="12.0.1"
ARCHIVE="v${VERSION}.tar.gz"
URL="https://github.com/AcademySoftwareFoundation/openvdb/archive/refs/tags/${ARCHIVE}"

mkdir -p source
cd source

if [ -f "$ARCHIVE" ]; then
    file_type=$(file -b --mime-type "$ARCHIVE")
    if [[ "$file_type" != "application/gzip" ]]; then
        echo "⚠️ Removing invalid archive: $ARCHIVE"
        rm -f "$ARCHIVE"
    fi
fi

if [ ! -f "$ARCHIVE" ]; then
    echo "📥 Downloading OpenVDB ${VERSION}..."
    curl -L -o "$ARCHIVE" "$URL"
fi

rm -rf openvdb-${VERSION}
tar -xzf "$ARCHIVE"

echo "✅ OpenVDB source ready"

