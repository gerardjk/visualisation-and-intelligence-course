# User Stories Guide

## Why user stories matter

Personas describe who the user is. User stories describe what the user needs to do.

A visualisation is stronger when every chart and interaction supports a user story.

## Format

```text
As a [type of user], I want to [do something], so that I can [make a decision / understand something / take an action].
```

## Examples

```text
As a transport policy adviser, I want to compare patronage recovery by mode since 2019, so that I can identify which services remain below baseline.
```

```text
As a local journalist, I want to see which suburbs have the largest rent increases, so that I can report where affordability pressure is concentrated.
```

```text
As a reviewer, I want to see the data source and limitations, so that I can judge whether the app is appropriate for my use.
```

## User story to feature map

| User story | App feature | Visual Vocabulary category | Risk |
|---|---|---|---|
| compare recovery over time | mode filter + line chart | change over time | methodology break |
| identify weakest recovery | ranked bar chart | ranking | ignores uncertainty |
| check source and caveats | disclosure expander | documentation/trust | vague limitations |

## Acceptance test

For each user story, answer:

```text
Can the user complete the task in the app?
What data is required?
What interaction is required?
What could fail?
How does the app guide the user if it fails?
```
