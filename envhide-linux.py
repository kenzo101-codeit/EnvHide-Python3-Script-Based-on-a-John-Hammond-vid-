#!/usr/bin/env python3

import os
import random
import string
from pprint import pprint

env_vars = [
    "PATH",
    "PWD",
    "OLDPWD",
    "SHELL",
    "TERM",
    "SHLVL",
    "HOSTNAME",
    "LANG",
    "TMPDIR",
    "LD_LIBRARY_PATH",
    "MANPATH",
]

# Build ENV mapping dictionary:
# env_mapping[character][variable] = [indices where that character appears]
env_mapping = {}

for character in string.printable:
    env_mapping[character] = {}
    for var in env_vars:
        value = os.getenv(var)
        if not value:
            continue

        if character in value:
            env_mapping[character][var] = [
                i for i, c in enumerate(value) if c == character
            ]


def envhide_obfuscate(text):
    obf_code = []

    for c in text:
        possible_vars = list(env_mapping.get(c, {}).keys())

        if not possible_vars:
            obf_code.append(f"[char]{ord(c)}")
            continue

        chosen_var = random.choice(possible_vars)
        possible_indices = env_mapping[c][chosen_var]

        if not possible_indices:
            obf_code.append(f"[char]{ord(c)}")
            continue

        chosen_index = random.choice(possible_indices)

        # PowerShell syntax to read a character from an environment variable
        pwsh_syntax = f"$env:{chosen_var}[{chosen_index}]"
        obf_code.append(pwsh_syntax)

    return obf_code


def powershell_obfuscate(text):
    iex = envhide_obfuscate("iex")
    pieces = envhide_obfuscate(text)

    iex_stage = f'& {"".join(iex)} -Join ${random.randint(1, 99999)}'
    payload_stage = f'& {"".join(pieces)} -Join ${random.randint(1, 99999)}'

    return f"& {iex_stage} {payload_stage}"


pwsh_command = "Write-Output 420"

pprint(envhide_obfuscate(pwsh_command))
