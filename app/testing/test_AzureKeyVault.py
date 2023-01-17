from AzureKeyVault import AzureKeyVault

def test_get_secret_key_vault_reference_returns_correct_reference():
    key_vault = AzureKeyVault("https://example.com")
    secret_name = "my-secret"
    expected_value = "@Microsoft.KeyVault(SecretUri=https://example.com/secrets/my-secret/)"

    actual_value = key_vault.get_secret_key_vault_reference("my-secret")

    assert actual_value == expected_value

def test_get_key_vault_secret_id_returns_appropriate_secret_id_for_keyvault():
    module = "identity"
    variable_name = "DB_PASSWORD"
    
    expected_value = "identity-db-password"

    actual_value = AzureKeyVault("https://example.com").get_key_vault_secret_id("identity", "DB_PASSWORD")

    assert actual_value == expected_value