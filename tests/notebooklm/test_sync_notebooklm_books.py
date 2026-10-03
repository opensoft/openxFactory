"""Retained carve/discovery entry point for focused NotebookLM scenarios.

Forwarders execute the extracted scenario bodies with their original setup and
cleanup. Non-collectable support modules own those bodies; each scenario runs
once. This preserves the explicit 137-method retained floor and module ceiling.
"""

from __future__ import annotations

from tests.notebooklm import _test_hosting_declaration_support as _group_0
from tests.notebooklm import _test_hosting_paths_support as _group_1
from tests.notebooklm import _test_hosting_refusal_support as _group_2
from tests.notebooklm import _test_lifecycle_books_support as _group_3
from tests.notebooklm import _test_profile_binding_support as _group_4
from tests.notebooklm import _test_projection_document_parity_support as _group_5
from tests.notebooklm import _test_projection_titles_support as _group_6
from tests.notebooklm import _test_root_products_support as _group_7
from tests.notebooklm import _test_session_import_binding_support as _group_8
from tests.notebooklm import _test_session_notebook_import_support as _group_9
from tests.notebooklm import _test_session_notebook_lifecycle_support as _group_10
from tests.notebooklm import _test_session_notebook_refresh_support as _group_11
from tests.notebooklm import _test_session_sweep_support as _group_12
from tests.notebooklm import _test_source_import_boundaries_support as _group_14
from tests.notebooklm import _test_source_import_support as _group_13
from tests.notebooklm import _test_upload_readiness_support as _group_15


class HostingDeclarationTests(_group_0.HostingDeclarationTests):
    def test_undeclared_install_is_reported_as_a_transition_state_not_a_case(self) -> None: self.scenario_undeclared_install_is_reported_as_a_transition_state_not_a_case()
    def test_declared_profile_active_binds_the_run(self) -> None: self.scenario_declared_profile_active_binds_the_run()
    def test_a_run_pointed_at_another_account_refuses(self) -> None: self.scenario_a_run_pointed_at_another_account_refuses()
    def test_an_unreadable_profile_refuses_rather_than_guessing(self) -> None: self.scenario_an_unreadable_profile_refuses_rather_than_guessing()
    def test_a_pending_migration_binds_to_the_account_that_holds_the_books(self) -> None: self.scenario_a_pending_migration_binds_to_the_account_that_holds_the_books()
    def test_a_pending_migration_still_refuses_a_third_account(self) -> None: self.scenario_a_pending_migration_still_refuses_a_third_account()
    def test_the_reader_ignores_comments_and_nested_blocks(self) -> None: self.scenario_the_reader_ignores_comments_and_nested_blocks()


class ParityReportTests(_group_0.ParityReportTests):
    def test_a_book_missing_a_derived_title_fails_parity(self) -> None: self.scenario_a_book_missing_a_derived_title_fails_parity()
    def test_matching_books_prove_parity_with_nothing_pending(self) -> None: self.scenario_matching_books_prove_parity_with_nothing_pending()
    def test_parity_never_mutates(self) -> None: self.scenario_parity_never_mutates()
    def test_a_non_string_profile_answer_is_unknown_not_a_crash(self) -> None: self.scenario_a_non_string_profile_answer_is_unknown_not_a_crash()


class TheDeclarationsPathResolvesFromConfigurationTests(_group_1.TheDeclarationsPathResolvesFromConfigurationTests):
    def test_the_env_var_resolves_the_declaration(self) -> None: self.scenario_the_env_var_resolves_the_declaration()
    def test_a_workspace_relative_env_var_resolves_from_the_root(self) -> None: self.scenario_a_workspace_relative_env_var_resolves_from_the_root()
    def test_the_workspace_configuration_resolves_the_declaration(self) -> None: self.scenario_the_workspace_configuration_resolves_the_declaration()
    def test_the_env_var_wins_over_the_workspace_configuration(self) -> None: self.scenario_the_env_var_wins_over_the_workspace_configuration()
    def test_absent_configuration_is_undeclared_and_does_not_break(self) -> None: self.scenario_absent_configuration_is_undeclared_and_does_not_break()
    def test_a_configured_path_that_does_not_exist_is_undeclared(self) -> None: self.scenario_a_configured_path_that_does_not_exist_is_undeclared()
    def test_a_configured_path_resolving_to_the_shipped_example_is_refused(self) -> None: self.scenario_a_configured_path_resolving_to_the_shipped_example_is_refused()
    def test_the_marker_is_read_from_the_record_not_from_the_path(self) -> None: self.scenario_the_marker_is_read_from_the_record_not_from_the_path()
    def test_the_shipped_example_is_not_the_last_resort(self) -> None: self.scenario_the_shipped_example_is_not_the_last_resort()
    def test_a_record_marked_live_binds(self) -> None: self.scenario_a_record_marked_live_binds()
    def test_an_empty_environment_value_is_unset(self) -> None: self.scenario_an_empty_environment_value_is_unset()


class UnreadableDeclarationFailsClosedTests(_group_2.UnreadableDeclarationFailsClosedTests):
    def test_an_existing_file_always_yields_a_dict_never_none(self) -> None: self.scenario_an_existing_file_always_yields_a_dict_never_none()
    def test_an_absent_file_is_the_only_undeclared_case(self) -> None: self.scenario_an_absent_file_is_the_only_undeclared_case()
    def test_each_unreadable_shape_refuses_instead_of_running_unbound(self) -> None: self.scenario_each_unreadable_shape_refuses_instead_of_running_unbound()


class MigrationStateVocabularyTests(_group_2.MigrationStateVocabularyTests):
    def test_an_unrecognized_state_is_refused(self) -> None: self.scenario_an_unrecognized_state_is_refused()
    def test_pending_and_complete_are_both_accepted(self) -> None: self.scenario_pending_and_complete_are_both_accepted()
    def test_a_pending_migration_without_a_from_profile_is_refused(self) -> None: self.scenario_a_pending_migration_without_a_from_profile_is_refused()
    def test_the_top_level_profile_is_required_even_while_pending(self) -> None: self.scenario_the_top_level_profile_is_required_even_while_pending()


class ProfileAccountIsCheckedWhenTheCliRecordedOneTests(_group_2.ProfileAccountIsCheckedWhenTheCliRecordedOneTests):
    def test_a_recorded_address_is_read(self) -> None: self.scenario_a_recorded_address_is_read()
    def test_a_null_address_is_unknown_not_empty_string(self) -> None: self.scenario_a_null_address_is_unknown_not_empty_string()
    def test_a_missing_profile_directory_is_unknown(self) -> None: self.scenario_a_missing_profile_directory_is_unknown()
    def test_the_right_profile_name_signed_in_as_the_wrong_account_refuses(self) -> None: self.scenario_the_right_profile_name_signed_in_as_the_wrong_account_refuses()
    def test_an_unknown_address_is_reported_not_treated_as_a_mismatch(self) -> None: self.scenario_an_unknown_address_is_reported_not_treated_as_a_mismatch()


class SplitIdeationBookTests(_group_3.SplitIdeationBookTests):
    def test_seeds_never_create_a_book(self) -> None: self.scenario_seeds_never_create_a_book()
    def test_dry_run_reports_pending_creation_and_mutates_nothing(self) -> None: self.scenario_dry_run_reports_pending_creation_and_mutates_nothing()
    def test_apply_creates_seeds_and_writes_the_workspace_record(self) -> None: self.scenario_apply_creates_seeds_and_writes_the_workspace_record()
    def test_missing_alias_resolves_by_title_and_reregisters(self) -> None: self.scenario_missing_alias_resolves_by_title_and_reregisters()
    def test_over_cap_projects_the_prefix_and_reports_the_exact_excess(self) -> None: self.scenario_over_cap_projects_the_prefix_and_reports_the_exact_excess()
    def test_oversized_source_rides_a_file_and_is_renamed_to_its_title(self) -> None: self.scenario_oversized_source_rides_a_file_and_is_renamed_to_its_title()
    def test_low_headroom_warns_and_names_the_owed_delta(self) -> None: self.scenario_low_headroom_warns_and_names_the_owed_delta()


class ProfileBindingHoldsForTheWholeRunTests(_group_4.ProfileBindingHoldsForTheWholeRunTests):
    def test_the_configured_profile_is_read_from_the_file(self) -> None: self.scenario_the_configured_profile_is_read_from_the_file()
    def test_an_absent_config_is_unknown(self) -> None: self.scenario_an_absent_config_is_unknown()
    def test_an_unbound_run_asserts_nothing(self) -> None: self.scenario_an_unbound_run_asserts_nothing()
    def test_a_profile_switched_mid_run_refuses_the_next_invocation(self) -> None: self.scenario_a_profile_switched_mid_run_refuses_the_next_invocation()
    def test_the_cache_does_not_hide_a_switch(self) -> None: self.scenario_the_cache_does_not_hide_a_switch()


class DeclarationIsEnforcedOnTheOperationalPathTests(_group_4.DeclarationIsEnforcedOnTheOperationalPathTests):
    def test_a_service_account_is_refused_by_the_sync_itself(self) -> None: self.scenario_a_service_account_is_refused_by_the_sync_itself()
    def test_a_consumer_account_is_refused_for_the_operator_hosted_case(self) -> None: self.scenario_a_consumer_account_is_refused_for_the_operator_hosted_case()
    def test_an_account_outside_the_declared_domain_is_refused(self) -> None: self.scenario_an_account_outside_the_declared_domain_is_refused()
    def test_a_third_case_is_refused(self) -> None: self.scenario_a_third_case_is_refused()
    def test_a_conforming_declaration_binds_the_run(self) -> None: self.scenario_a_conforming_declaration_binds_the_run()
    def test_an_undeclared_install_releases_the_pin(self) -> None: self.scenario_an_undeclared_install_releases_the_pin()
    def test_a_self_hosted_personal_declaration_is_accepted(self) -> None: self.scenario_a_self_hosted_personal_declaration_is_accepted()
    def test_nlm_itself_reasserts_the_binding_before_running(self) -> None: self.scenario_nlm_itself_reasserts_the_binding_before_running()


class ParityProvesDocumentsTests(_group_5.ParityProvesDocumentsTests):
    def test_a_collapsed_title_fails_parity_though_the_title_sets_are_equal(self) -> None: self.scenario_a_collapsed_title_fails_parity_though_the_title_sets_are_equal()
    def test_the_injective_derivation_proves_parity_over_documents(self) -> None: self.scenario_the_injective_derivation_proves_parity_over_documents()


class TitleUniquenessTests(_group_6.TitleUniquenessTests):
    def test_the_fourteen_enumerated_titles_move_exactly_as_designed(self) -> None: self.scenario_the_fourteen_enumerated_titles_move_exactly_as_designed()
    def test_documents_outside_the_migration_keep_their_titles(self) -> None: self.scenario_documents_outside_the_migration_keep_their_titles()
    def test_every_book_derives_one_title_per_document(self) -> None: self.scenario_every_book_derives_one_title_per_document()
    def test_a_status_change_moves_no_other_title(self) -> None: self.scenario_a_status_change_moves_no_other_title()
    def test_a_unique_readme_still_carries_its_parent_directory(self) -> None: self.scenario_a_unique_readme_still_carries_its_parent_directory()
    def test_the_spec_and_grounding_families_are_outside_the_scope(self) -> None: self.scenario_the_spec_and_grounding_families_are_outside_the_scope()
    def test_a_record_document_qualifies_nobody(self) -> None: self.scenario_a_record_document_qualifies_nobody()
    def test_titles_are_derived_from_structure_not_from_a_rendered_path(self) -> None: self.scenario_titles_are_derived_from_structure_not_from_a_rendered_path()
    def test_reverting_the_rule_to_a_bare_stem_reds_the_injectivity_check(self) -> None: self.scenario_reverting_the_rule_to_a_bare_stem_reds_the_injectivity_check()
    def test_a_one_level_qualifier_leaves_the_checklists_pair_colliding(self) -> None: self.scenario_a_one_level_qualifier_leaves_the_checklists_pair_colliding()


class RootLevelGovernedProductTests(_group_7.RootLevelGovernedProductTests):
    def test_the_allowlist_matches_the_doc_health_authority(self) -> None: self.scenario_the_allowlist_matches_the_doc_health_authority()
    def test_a_pinned_and_present_root_product_is_found(self) -> None: self.scenario_a_pinned_and_present_root_product_is_found()
    def test_a_present_but_unpinned_root_product_is_not_found(self) -> None: self.scenario_a_present_but_unpinned_root_product_is_not_found()
    def test_a_pinned_but_absent_root_product_is_not_found(self) -> None: self.scenario_a_pinned_but_absent_root_product_is_not_found()
    def test_installs_are_never_admitted(self) -> None: self.scenario_installs_are_never_admitted()
    def test_no_gitmodules_admits_nothing(self) -> None: self.scenario_no_gitmodules_admits_nothing()
    def test_an_uninitialized_root_product_warns_instead_of_reading_empty(self) -> None: self.scenario_an_uninitialized_root_product_warns_instead_of_reading_empty()
    def test_governed_repo_paths_puts_root_products_before_the_factories(self) -> None: self.scenario_governed_repo_paths_puts_root_products_before_the_factories()
    def test_scan_derives_the_openxwallet_ideation_book(self) -> None: self.scenario_scan_derives_the_openxwallet_ideation_book()
    def test_scan_derives_the_openavatar_book_by_the_same_widening(self) -> None: self.scenario_scan_derives_the_openavatar_book_by_the_same_widening()
    def test_a_root_product_with_no_ideation_document_derives_no_book(self) -> None: self.scenario_a_root_product_with_no_ideation_document_derives_no_book()
    def test_session_repositories_keeps_its_stated_agreement_with_scan(self) -> None: self.scenario_session_repositories_keeps_its_stated_agreement_with_scan()
    def test_the_workbench_sweep_sees_a_root_products_manifests(self) -> None: self.scenario_the_workbench_sweep_sees_a_root_products_manifests()


class SessionImportBindingTests(_group_8.SessionImportBindingTests):
    def test_a_session_notebook_cannot_import_into_the_served_checkout(self) -> None: self.scenario_a_session_notebook_cannot_import_into_the_served_checkout()
    def test_a_session_notebook_cannot_import_into_another_sessions_worktree(self) -> None: self.scenario_a_session_notebook_cannot_import_into_another_sessions_worktree()
    def test_a_non_session_notebook_cannot_import_into_a_session_worktree(self) -> None: self.scenario_a_non_session_notebook_cannot_import_into_a_session_worktree()
    def test_a_dead_sessions_directory_is_not_a_live_session(self) -> None: self.scenario_a_dead_sessions_directory_is_not_a_live_session()
    def test_the_import_cannot_feed_itself(self) -> None: self.scenario_the_import_cannot_feed_itself()
    def test_a_draft_only_outline_source_still_imports_and_commits(self) -> None: self.scenario_a_draft_only_outline_source_still_imports_and_commits()


class SessionNotebookImportTests(_group_9.SessionNotebookImportTests):
    def test_an_import_lands_in_the_worktree_on_the_session_branch(self) -> None: self.scenario_an_import_lands_in_the_worktree_on_the_session_branch()
    def test_an_import_refuses_a_worktree_that_drifted_during_the_fetch(self) -> None: self.scenario_an_import_refuses_a_worktree_that_drifted_during_the_fetch()
    def test_a_nested_factory_session_import_keeps_the_repository_name(self) -> None: self.scenario_a_nested_factory_session_import_keeps_the_repository_name()


class SessionNotebookQuotaTests(_group_9.SessionNotebookQuotaTests):
    def test_an_exhausted_quota_still_opens_the_session(self) -> None: self.scenario_an_exhausted_quota_still_opens_the_session()
    def test_the_notice_speaks_of_concurrent_tiles_across_everyone(self) -> None: self.scenario_the_notice_speaks_of_concurrent_tiles_across_everyone()
    def test_with_quota_room_the_session_opens_with_its_notebook(self) -> None: self.scenario_with_quota_room_the_session_opens_with_its_notebook()
    def test_a_plane_with_no_adapter_creates_nothing_and_says_nothing(self) -> None: self.scenario_a_plane_with_no_adapter_creates_nothing_and_says_nothing()


class SessionNotebookAliasTests(_group_10.SessionNotebookAliasTests):
    def test_session_notebook_is_created_from_the_worktree_under_the_exact_alias(self) -> None: self.scenario_session_notebook_is_created_from_the_worktree_under_the_exact_alias()
    def test_a_session_over_the_provider_source_cap_is_refused_before_any_mutation(self) -> None: self.scenario_a_session_over_the_provider_source_cap_is_refused_before_any_mutation()
    def test_the_same_branch_in_a_second_repository_gets_a_different_alias(self) -> None: self.scenario_the_same_branch_in_a_second_repository_gets_a_different_alias()
    def test_a_branch_with_no_live_worktree_is_refused_not_invented(self) -> None: self.scenario_a_branch_with_no_live_worktree_is_refused_not_invented()
    def test_the_transcribed_container_suffix_is_the_productions_own(self) -> None: self.scenario_the_transcribed_container_suffix_is_the_productions_own()
    def test_the_session_namespace_is_disjoint_from_the_swept_one(self) -> None: self.scenario_the_session_namespace_is_disjoint_from_the_swept_one()


class SessionNotebookSweepSafetyTests(_group_10.SessionNotebookSweepSafetyTests):
    def test_orphan_sweep_never_takes_a_live_session_notebook(self) -> None: self.scenario_orphan_sweep_never_takes_a_live_session_notebook()
    def test_the_dry_run_plan_never_names_a_session_notebook(self) -> None: self.scenario_the_dry_run_plan_never_names_a_session_notebook()
    def test_the_dry_run_says_the_account_is_UNREADABLE_not_that_it_is_empty(self) -> None: self.scenario_the_dry_run_says_the_account_is_UNREADABLE_not_that_it_is_empty()
    def test_a_session_leaves_no_manifest_that_could_disable_the_sweep(self) -> None: self.scenario_a_session_leaves_no_manifest_that_could_disable_the_sweep()


class SessionNotebookBookIsolationTests(_group_11.SessionNotebookBookIsolationTests):
    def test_session_worktrees_are_outside_every_book_with_pins_present(self) -> None: self.scenario_session_worktrees_are_outside_every_book_with_pins_present()
    def test_session_worktrees_are_outside_every_book_without_pins(self) -> None: self.scenario_session_worktrees_are_outside_every_book_without_pins()
    def test_a_session_source_set_and_a_book_share_no_document(self) -> None: self.scenario_a_session_source_set_and_a_book_share_no_document()


class SessionNotebookRefreshTests(_group_11.SessionNotebookRefreshTests):
    def test_refresh_resyncs_from_the_worktree_without_recreating(self) -> None: self.scenario_refresh_resyncs_from_the_worktree_without_recreating()
    def test_the_dry_run_prints_a_plan_touches_nothing_and_is_not_book_drift(self) -> None: self.scenario_the_dry_run_prints_a_plan_touches_nothing_and_is_not_book_drift()
    def test_session_end_retires_the_notebook_and_never_repoints_it_at_main(self) -> None: self.scenario_session_end_retires_the_notebook_and_never_repoints_it_at_main()
    def test_the_teardown_seam_retires_through_the_real_adapter(self) -> None: self.scenario_the_teardown_seam_retires_through_the_real_adapter()
    def test_retire_refuses_to_cross_into_the_reference_set_namespace(self) -> None: self.scenario_retire_refuses_to_cross_into_the_reference_set_namespace()


class SessionSweepTests(_group_12.SessionSweepTests):
    def test_the_classifier_answers_three_ways_and_ignores_non_sessions(self) -> None: self.scenario_the_classifier_answers_three_ways_and_ignores_non_sessions()
    def test_scope_is_tested_by_prefix_not_by_splitting_on_hyphens(self) -> None: self.scenario_scope_is_tested_by_prefix_not_by_splitting_on_hyphens()
    def test_a_live_alias_is_never_dead_however_lossy_the_transform(self) -> None: self.scenario_a_live_alias_is_never_dead_however_lossy_the_transform()
    def test_an_unaccountable_repository_refuses_and_retires_nothing(self) -> None: self.scenario_an_unaccountable_repository_refuses_and_retires_nothing()
    def test_an_unreadable_notebook_list_refuses_and_retires_nothing(self) -> None: self.scenario_an_unreadable_notebook_list_refuses_and_retires_nothing()
    def test_the_report_is_the_default_and_retires_nothing(self) -> None: self.scenario_the_report_is_the_default_and_retires_nothing()
    def test_apply_retires_exactly_the_dead_set(self) -> None: self.scenario_apply_retires_exactly_the_dead_set()
    def test_an_adapter_without_retire_refuses_loudly(self) -> None: self.scenario_an_adapter_without_retire_refuses_loudly()
    def test_a_workspace_with_no_session_repositories_retires_nothing(self) -> None: self.scenario_a_workspace_with_no_session_repositories_retires_nothing()
    def test_the_two_session_modes_are_mutually_exclusive(self) -> None: self.scenario_the_two_session_modes_are_mutually_exclusive()
    def test_a_session_opened_from_a_feature_worktree_is_seen_as_live(self) -> None: self.scenario_a_session_opened_from_a_feature_worktree_is_seen_as_live()
    def test_session_ref_sees_a_session_opened_from_a_feature_worktree(self) -> None: self.scenario_session_ref_sees_a_session_opened_from_a_feature_worktree()


class NotebookLmSourceImportBoundaryTests(_group_14.NotebookLmSourceImportBoundaryTests):
    def test_hostile_export_titles_cannot_traverse_the_workspace(self) -> None: self.scenario_hostile_export_titles_cannot_traverse_the_workspace()
    def test_scan_excludes_worktree_containers_and_nested_checkouts(self) -> None: self.scenario_scan_excludes_worktree_containers_and_nested_checkouts()
    def test_append_import_refuses_paths_outside_workspace(self) -> None: self.scenario_append_import_refuses_paths_outside_workspace()


class NotebookLmSourceImportTests(_group_13.NotebookLmSourceImportTests):
    def test_parse_export_title_still_supports_explicit_route(self) -> None: self.scenario_parse_export_title_still_supports_explicit_route()
    def test_import_new_sources_dry_run_pulls_all_non_seed_sources(self) -> None: self.scenario_import_new_sources_dry_run_pulls_all_non_seed_sources()
    def test_import_new_sources_writes_to_origin_folder_and_dedupes(self) -> None: self.scenario_import_new_sources_writes_to_origin_folder_and_dedupes()
    def test_proposal_origin_imports_as_draft_and_dedupes(self) -> None: self.scenario_proposal_origin_imports_as_draft_and_dedupes()
    def test_rejects_archived_or_missing_proposal_origin(self) -> None: self.scenario_rejects_archived_or_missing_proposal_origin()


class UploadReadinessTests(_group_15.UploadReadinessTests):
    def test_a_slow_rename_is_polled_until_it_takes(self) -> None: self.scenario_a_slow_rename_is_polled_until_it_takes()
    def test_a_rename_that_never_takes_fails_LOUDLY(self) -> None: self.scenario_a_rename_that_never_takes_fails_LOUDLY()
    def test_a_rerun_ADOPTS_the_stray_instead_of_adding_a_duplicate(self) -> None: self.scenario_a_rerun_ADOPTS_the_stray_instead_of_adding_a_duplicate()
    def test_a_stray_whose_CONTENT_differs_is_left_alone(self) -> None: self.scenario_a_stray_whose_CONTENT_differs_is_left_alone()
    def test_a_DUPLICATE_TITLE_does_not_satisfy_the_rename_verifier(self) -> None: self.scenario_a_DUPLICATE_TITLE_does_not_satisfy_the_rename_verifier()
    def test_adoption_UNWRAPS_a_json_wrapped_body_before_hashing(self) -> None: self.scenario_adoption_UNWRAPS_a_json_wrapped_body_before_hashing()
    def test_the_content_digest_is_one_mechanism_for_both_sides(self) -> None: self.scenario_the_content_digest_is_one_mechanism_for_both_sides()
