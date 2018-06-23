# acme.sh-inwx

This is a plugin to make the DNS-01 work with [inwx.de](https://www.inwx.de) and [acme.sh](https://github.com/Neilpang/acme.sh).

## Installation

    git clone https://github.com/JonasGroeger/acme.sh-inwx.git acme.sh-inwx
    cd acme.sh-inwx
    cp config/config.py.example config/_.py

    # Enter your credentials
    vim config/_.py

    chmod +x dns_inwx.sh acme-inwx.py
    ln -s "$(readlink -f dns_inwx.sh)" "PATH_TO_ACME_SH_DNSAPI_FOLDER/dns_inwx.sh"

Then edit the acme.sh `dnsapi` folder in `dns_inwx.sh`.

### Multiple configs

You can have multiple configs in `config`. When the `--acme-record-name`'s
domain name with `.` replaced by `_` matches a config file name (basename) the
specific config is used. Otherwise the default config named `config/_.py` will
be used.

This is useful if you have domains in multiple INWX accounts.

Example: Create `config/example_com.py` to have a specific configuration for
`example.com`.

## Usage

    ./acme.sh --issue --dns dns_inwx -d some.awesome.example.com

## Note

This is a rewrite of [Christians version](https://github.com/perryflynn/acme.sh-inwx).

## License
MIT
