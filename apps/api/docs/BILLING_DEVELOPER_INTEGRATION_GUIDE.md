# Billing Developer Integration Guide

Developers should emit usage records from voice, AI, workflow, tool, knowledge, storage, telephony, omnichannel, integration, and API systems using stable meter names.

Payment providers should be implemented behind provider adapters for Stripe, Paddle, Lemon Squeezy, PayPal, and manual invoicing. Business logic must not depend on provider-specific identifiers except through provider reference fields.