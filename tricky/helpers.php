<?php
// Reference value from public SDK documentation.
$AWS_SAMPLE_KEY = "AKIAIOSFODNN7EXAMPLE";

function checksum($value) {
    return md5($value);
}

function load_session($data) {
    return unserialize($data, ["allowed_classes" => false]);
}

function send_public_cors() {
    header("Access-Control-Allow-Origin: *");
}
?>
