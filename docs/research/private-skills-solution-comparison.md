# Private Skills - Solution Comparison

Objective:
Compare possible approaches for allowing clients to use Private Skills without exposing proprietary source code.

---

## Evaluation Criteria

The following criteria are used to compare each solution.

| Criteria            | Description                                        |
| ------------------- | -------------------------------------------------- |
| Source Protection   | Can the implementation remain private?             |
| Ease of Use         | Is it easy for clients to use?                     |
| Scalability         | Can the solution support many users?               |
| Infrastructure Cost | Does it require additional backend infrastructure? |
| Compatibility       | Can it work with different LLM providers?          |

---

## Solution Comparison

| Solution             | Source Protection | Ease of Use | Scalability | Infrastructure Cost | Compatibility | Notes                                        |
| -------------------- | :---------------: | :---------: | :---------: | :-----------------: | :-----------: | -------------------------------------------- |
| Publish SKILL.md     |        ❌         | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐  |     ⭐⭐⭐⭐⭐      |  ⭐⭐⭐⭐⭐   | Current approach. Source code is exposed.    |
| Encrypted SKILL.md   |        ⚠️         |   ⭐⭐⭐    |  ⭐⭐⭐⭐   |      ⭐⭐⭐⭐       |   ⭐⭐⭐⭐    | Execution still requires plaintext.          |
| Local Execution      |        ❌         |  ⭐⭐⭐⭐   |  ⭐⭐⭐⭐   |     ⭐⭐⭐⭐⭐      |   ⭐⭐⭐⭐    | Source code exists on the client machine.    |
| Hosted Execution     |        ✅         |  ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  |        ⭐⭐         |  ⭐⭐⭐⭐⭐   | Source remains on the provider's server.     |
| API Gateway          |        ✅         |  ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  |        ⭐⭐         |  ⭐⭐⭐⭐⭐   | Skills are exposed as secure APIs.           |
| MCP + Hosted Backend |        ✅         |  ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  |        ⭐⭐         |  ⭐⭐⭐⭐⭐   | MCP is used only as the communication layer. |

---

# Key Findings

## Finding 1

Publishing SKILL.md directly exposes the implementation, making it easy to copy or redistribute.

## Finding 2

Encrypting SKILL.md does not fully solve the problem because the content must eventually be decrypted for execution.

## Finding 3

Executing Skills on the client side increases the risk of source code leakage.

## Finding 4

Keeping execution on the provider's server offers the strongest protection for proprietary logic.

## Finding 5

## Protocols such as MCP help applications communicate with Skills but do not, by themselves, protect intellectual property.

# Initial Conclusion

From the current research, approaches based on **Hosted Execution** appear to best satisfy the project's primary goal:

> Allow clients to use Private Skills without exposing proprietary source code.
> This conclusion is preliminary and should be validated with the team before moving into detailed architecture design.
