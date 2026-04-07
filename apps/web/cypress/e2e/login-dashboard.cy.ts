describe("NexusHR login and dashboard flow", () => {
  it("signs in with the seeded employee and loads the dashboard", () => {
    cy.visit("/login");
    cy.get('input[type="email"]').clear().type("maya.rao@nexushr.example");
    cy.get('input[type="password"]').clear().type("NexusHR!2026");
    cy.get('input[type="text"]').first().clear().type("246810");
    cy.contains("button", "Sign in securely").click();

    cy.url().should("include", "/dashboard");
    cy.contains("Employee Command Center").should("be.visible");
    cy.contains("Monthly Calendar").should("be.visible");
    cy.contains("Alerts & Notifications").should("be.visible");
  });
});
