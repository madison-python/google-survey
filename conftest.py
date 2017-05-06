import os
import betamax

cassettes_dir = 'tests/cassettes/'

if not os.path.exists(cassettes_dir):
    os.makedirs(cassettes_dir)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = cassettes_dir
