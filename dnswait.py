"""Script and library to wait for a DNS authority server to get its configuration.
"""

from time import sleep
import argparse

import dns.message
import dns.resolver
import dns.query
import dns.name

import logging

logger = logging.getLogger(__name__)

__version__ = "0.0.1"


def find_authority(qname):
    """Locate the autoritative name server for the given name using a stub
    resolver.
    """
    try:
        response = dns.resolver.resolve(qname, "NS")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return find_authority(".".join(qname.split(".")[1:]))
    return [
        (ns.target, a.address)
        for ns in response
        for a in dns.resolver.resolve(ns.target, "A")
    ]


def wait_dns(qname, rdtype, value):
    """Wait for the authoritative name server for the given domain to have
    the given value.
    """

    authorities = find_authority(qname)
    logger.info("%d authoritative name servers to check.", len(authorities))
    while authorities:
        authority_name, authority_address = authorities.pop(0)
        logger.debug("Checking %s", authority_name)
        response = dns.query.udp(
            dns.message.make_query(qname, rdtype), authority_address
        )
        if value in str(response):
            logger.debug("%s have the expected value!", authority_name)
        else:
            logger.debug(
                "%s don't have the expected value, will have to retry", authority_name
            )
            authorities.append((authority_name, authority_address))
            sleep(1)
    logger.info("All authoritative servers have the expected value.")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("type")
    parser.add_argument("expected")
    parser.add_argument("-v", action="count", default=0)
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(
        level=[logging.ERROR, logging.INFO, logging.DEBUG][min(args.v, 2)]
    )
    wait_dns(args.name, args.type, args.expected)


if __name__ == "__main__":
    main()
