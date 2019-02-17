"""
A calculator based on https://en.wikipedia.org/wiki/Reverse_Polish_notation
"""

from __future__ import print_function

from umbral import pre, keys, config, signing

# set the default curve
config.set_default_curve()


def test_pre(text):

    # Generate umbral keys for Alice.
    alice_private_key = keys.UmbralPrivateKey.gen_key()
    alice_public_key = alice_private_key.get_pubkey()
    alice_signing_key = keys.UmbralPrivateKey.gen_key()
    alice_verifying_key = alice_signing_key.get_pubkey()
    alice_signer = signing.Signer(private_key=alice_signing_key)

    # Generate umbral keys for Bob.
    bob_private_key = keys.UmbralPrivateKey.gen_key()
    bob_public_key = bob_private_key.get_pubkey()

    # Encrypt data with Alice’s public key.
    #plaintext = b'Proxy Re-encryption is cool!'
    plaintext = str.encode(text)
    ciphertext, capsule = pre.encrypt(alice_public_key, plaintext)

    # Test decryption with Alice's private key
    alice_cleartext = pre.decrypt(ciphertext=ciphertext,
                            capsule=capsule,
                            decrypting_key=alice_private_key)

    print("Alice's cleartext:")
    print(alice_cleartext)

    # Alice generates split re-encryption keys for Bob with “M of N”.
    kfrags = pre.generate_kfrags(delegating_privkey=alice_private_key,
                                 signer=alice_signer,
                                 receiving_pubkey=bob_public_key,
                                 threshold=10,
                                 N=20)

    #9
    # Ursulas perform re-encryption
    # ------------------------------
    # Bob asks several Ursulas to re-encrypt the capsule so he can open it. 
    # Each Ursula performs re-encryption on the capsule using the `kfrag` 
    # provided by Alice, obtaining this way a "capsule fragment", or `cfrag`.
    # Let's mock a network or transport layer by sampling `threshold` random `kfrags`,
    # one for each required Ursula.

    import random

    kfrags = random.sample(kfrags,  # All kfrags from above
                           10)      # M - Threshold

    # Bob collects the resulting `cfrags` from several Ursulas. 
    # Bob must gather at least `threshold` `cfrags` in order to activate the capsule.

    capsule.set_correctness_keys(delegating=alice_public_key,
                                     receiving=bob_public_key,
                                     verifying=alice_verifying_key)

    cfrags = list()  # Bob's cfrag collection
    for kfrag in kfrags:
        cfrag = pre.reencrypt(kfrag=kfrag, capsule=capsule)
        cfrags.append(cfrag)  # Bob collects a cfrag
        
    assert len(cfrags) == 10

    #10
    # Bob attaches cfrags to the capsule
    # ----------------------------------
    # Bob attaches at least `threshold` `cfrags` to the capsule;
    # then it can become *activated*.

    for cfrag in cfrags:
        capsule.attach_cfrag(cfrag)


    #11
    # Bob activates and opens the capsule
    # ------------------------------------
    # Finally, Bob activates and opens the capsule,
    # then decrypts the re-encrypted ciphertext.

    bob_cleartext = pre.decrypt(ciphertext=ciphertext, 
        capsule=capsule, 
        decrypting_key=bob_private_key)
    
    print("Bob's cleartext:")
    print(bob_cleartext)
    success = bob_cleartext == plaintext
    assert success

    return {
        "success": success, 
        "alice_cleartext": str(alice_cleartext, 'utf-8'),
        "bob_cleartext": str(bob_cleartext, 'utf-8')
        }




