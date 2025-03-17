jq -s '[.[][]]' ../4tier/data-reduced/train_valid/data.json ../social-network/data-nano/train_valid/data.json ../social-network-ut/data-super-reduced/train_valid/data.json > data-reduced/train_valid/data.json

jq -s '[.[][]]' ../4tier/data-reduced/validation_valid/data.json ../social-network/data-nano/validation_valid/data.json ../social-network-ut/data-super-reduced/validation_valid/data.json > data-reduced/validation_valid/data.json

jq -s '[.[][]]' ../4tier/data-reduced/test_valid/data.json ../social-network/data-nano/test_valid/data.json ../social-network-ut/data-super-reduced/test_valid/data.json > data-reduced/test_valid/data.json