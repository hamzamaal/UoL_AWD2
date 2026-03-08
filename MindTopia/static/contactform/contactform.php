<?php
declare(strict_types=1);

/**
 * Simple AJAX contact form handler.
 *
 * Expected POST fields:
 * - name
 * - email
 * - subject
 * - message
 *
 * Returns:
 * - "OK" on success
 * - plain-text error message on failure
 */

header('Content-Type: text/plain; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'Method not allowed.';
    exit;
}

/**
 * Sanitize text input.
 *
 * @param string|null $value
 * @return string
 */
function clean_input(?string $value): string
{
    return trim(strip_tags((string) $value));
}

$name = clean_input($_POST['name'] ?? '');
$email = clean_input($_POST['email'] ?? '');
$subject = clean_input($_POST['subject'] ?? '');
$message = trim((string) ($_POST['message'] ?? ''));

if ($name === '') {
    echo 'Please enter your name.';
    exit;
}

if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo 'Please enter a valid email address.';
    exit;
}

if ($subject === '') {
    echo 'Please enter a subject.';
    exit;
}

if ($message === '') {
    echo 'Please enter a message.';
    exit;
}

/*
 * Replace this with the destination email address you want to use.
 */
$to = 'your@email.com';

$email_subject = 'Website Contact: ' . $subject;

$email_body = "You have received a new message from your website contact form.\n\n";
$email_body .= "Name: {$name}\n";
$email_body .= "Email: {$email}\n";
$email_body .= "Subject: {$subject}\n\n";
$email_body .= "Message:\n{$message}\n";

$headers = [];
$headers[] = 'MIME-Version: 1.0';
$headers[] = 'Content-Type: text/plain; charset=UTF-8';
$headers[] = 'From: ' . $name . ' <' . $email . '>';
$headers[] = 'Reply-To: ' . $email;
$headers[] = 'X-Mailer: PHP/' . phpversion();

$sent = mail(
    $to,
    $email_subject,
    $email_body,
    implode("\r\n", $headers)
);

if ($sent) {
    echo 'OK';
} else {
    echo 'Message could not be sent. Please try again later.';
}