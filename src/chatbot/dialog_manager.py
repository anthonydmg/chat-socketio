from .utils import matching_entity
from .dialog_tracker import DialogTracker

THESHOLD_CONFIDENCE = 0.5
ENTITIES_PROCEDIMIENTOS = ["retiro total", "reincorporacion", "retiro parcial","reserva de matricula"]
ENTITIES_CONSTANCIAS = ["constancia de notas","constancia de matricula", "constancia de estudios"]

class DialogManagement:

    def inference_rules(self, intent_name, intent_score, entities, last_message_user, last_message_bot):
        responses = []
        print(f"\nIntent: {intent_name}\n")

        print(f"\nEntities: {entities}\n")


        utters_requerir = ["utter_requerir_entidad_procedimiento_costo", "utter_requerir_entidad_procedimiento_formato", "utter_requerir_entidad_procedimiento_fechas"]
        if last_message_bot!= None and (last_message_bot['utter_response'] in utters_requerir) and len(entities) > 0:
            intent_name = last_message_user["intent_name"]

        elif intent_score < THESHOLD_CONFIDENCE: ## Manejo de confianza 
            if last_message_bot!= None and last_message_bot['utter_response'] == "utter_ask_rephrase":
                responses = [ {"response": "utter_fuera_alcance"},
                              {"response": "utter_recuerda_escribir_ayuda"}]
            else:
                responses = [{"response": "utter_ask_rephrase"}]
            return responses

        if intent_name == "comenzar_dialogo":
            responses = [{"response": "utter_saludo"},
                         {"response": "utter_recuerda_escribir_ayuda"},
                         {"response": "utter_requerir_consulta"}]
                         
        elif intent_name == "saludo":
            responses = [{"response": "utter_saludo"},
                         {"response": "utter_requerir_consulta"}]

        elif intent_name == "despedida":
            responses = [{"response": "utter_despedida"}]

        elif intent_name == "denegar_mas_ayuda":
            responses = [{"response": "utter_despedida"}]

        elif intent_name == "confirmar_requerir_mas_ayuda":
            responses = [{"response": "utter_requerir_consulta"}]
        
        if intent_name == "costo_tramite_procedimiento":
            
            if len(entities) == 0:
                ## caso contextual
                last_intent_name = last_message_user["intent_name"]
                print("last_intent_name:", last_intent_name)
                if last_intent_name == "reincorporacion__fechas" or last_intent_name == "reincorporacion__procedimiento":
                    responses = [{"response":"utter_reincorporacion__costo"},
                                 {"response": "utter_requerir_consulta"}]

                elif last_intent_name == "utter_retiro_total__fechas"  or last_intent_name == "retiro_total__procedimiento":
                    responses = [{"response":"utter_retiro_total__costo"},
                                 {"response": "utter_requerir_consulta"}]
                
                elif last_intent_name == "utter_retiro_parcial__fechas" or last_intent_name == "retiro_parcial__procedimiento":
                    responses = [{"response":"utter_retiro_parcial__costo"},
                                 {"response": "utter_requerir_consulta"}]
                
                elif last_intent_name == "constancia_matricula__formato_solicitud" or last_intent_name == "constancia_matricula__solicitud_procedimiento":
                    responses = [{"response":"utter_constancia_matricula__costo"},
                                 {"response": "utter_requerir_consulta"}]
                else:
                    responses = [{"response": "utter_requerir_entidad_procedimiento_costo"}]
                
                return responses
            
            else:
                entity_value = entities[0]["value"]
                entity, score = matching_entity(entity_value, ENTITIES_PROCEDIMIENTOS + ENTITIES_CONSTANCIAS)
                
                if score < 0.6:
                    responses = [{"response":"utter_fuera_alcance_procedimiento_tramite"},
                                 {"response": "utter_recuerda_escribir_ayuda"},
                                 {"response": "utter_sugerir_contactar_aera"}
                                ]
                    return responses

                if entity == "retito_total":
                    responses = [{"response": "utter_retiro_total__costo"},
                                 {"response": "utter_requerir_consulta"}]

                elif entity == "retito_parcial":
                    responses = [{"response": "utter_retiro_parcial__costo"},
                                  {"response": "utter_requerir_consulta"}]
                
                elif entity == "reincorporacion":
                    responses = [{"response":"utter_reincorporacion__costo"},
                                 {"response": "utter_requerir_consulta"}]
                
                elif entity == "constancia_matricula":
                    responses = [{"response":"utter_constancia_matricula__costo"},
                                 {"response": "utter_requerir_consulta"}]
                
                else:
                    responses = [{"response":"utter_fuera_alcance_procedimiento_tramite"},
                                 {"response": "utter_recuerda_escribir_ayuda"},
                                 {"response": "utter_sugerir_contactar_aera"}
                                  ]
                return responses

        if intent_name == "formato_solicitud":
            
            if len(entities) == 0:
                responses = [{"response": "utter_requerir_entidad_procedimiento_formato"}]
                return responses
            
            else:
                entity_value = entities[0]["value"]
                entity, score = matching_entity(entity_value, ENTITIES_PROCEDIMIENTOS + ENTITIES_CONSTANCIAS)
                
                if score < 0.6:
                    responses = [{"response":"utter_fuera_alcance_procedimiento_tramite"},
                                 {"response": "utter_recuerda_escribir_ayuda"},
                                 {"response": "utter_sugerir_contactar_aera"}
                                ]
                    return responses

                if entity == "retito_total":
                    responses = [{"response": "utter_retiro_total__formato_solicitud"}, 
                                 {"response": "utter_requerir_mas"}]

                elif entity == "retito_parcial":
                    responses = [{"response": "utter_retiro_parcial__formato_solicitud"},
                                 {"response": "utter_requerir_mas"}]
                
                elif entity == "reincorporacion":
                    responses = [{"response":"utter_reincorporacion__formato_solicitud"},
                                 {"response": "utter_requerir_mas"}]
                
                elif entity == "constancia_matricula":
                    responses = [{"response":"utter_constancia_matricula__formato_solicitud"},
                                 {"response": "utter_requerir_mas"}]
                
                else:
                    responses = [{"response":"utter_fuera_alcance_procedimiento_tramite"},
                                 {"response": "utter_recuerda_escribir_ayuda"},
                                 {"response": "utter_sugerir_contactar_aera"}
                                  ]
                return responses
        
        
        ## Hacer uno por uno y poner el slot

        if intent_name == "retiro_parcial__fechas":
            responses = [{"response": "utter_retiro_parcial__fechas"},
                         {"response": "utter_requerir_mas"}]

    
        if intent_name == "reincorporacion__fechas":
            responses = [{"response": "utter_reincorporacion__fechas"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "retiro_total__fechas":
            responses = [{"response": "utter_retiro_total__fechas"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "reserva_matricula__fechas":
                    responses = [{"response": "utter_reserva_matricula__fechas"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "pago_autoseguro__fechas":
            responses = [{"response": "utter_pago_autoseguro__fechas"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "matricula_procedimiento":
            responses = [{"response": "utter_matricula_procedimiento"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "carnet_universitario__solicitud":
                    responses = [{"response": "utter_carnet_universitario__solicitud"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "matricula__cronograma":
            responses = [{"response": "utter_matricula__cronograma"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "matricula__horarios":
            responses = [{"response": "utter_matricula__horarios"},
                        {"response": "utter_requerir_mas"}]

        if intent_name == "pago_autoseguro_procedimiento":
                    responses = [{"response": "utter_pago_autoseguro_procedimiento"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "perdida_turno_matricula":
            responses = [{"response": "utter_perdida_turno_matricula"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "matricula_rezagada__procedimiento":
            responses = [{"response": "utter_matricula_rezagada__procedimiento"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "cambio_seccion":
                    responses = [{"response": "utter_cambio_seccion"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "cursos_horarios":
            responses = [{"response": "utter_cursos_horarios"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "retiro_parcial__procedimiento":
            responses = [{"response": "utter_retiro_parcial__procedimiento"},
                        {"response": "utter_requerir_mas"}]

        if intent_name == "retiro_parcial__unico_curso":
                    responses = [{"response": "utter_retiro_parcial__unico_curso"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "retiro_parcial__maximo_cursos":
            responses = [{"response": "utter_retiro_parcial__maximo_cursos"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "retiro_total__requisitos_documentos_justificacion":
            responses = [{"response": "utter_retiro_total__requisitos_documentos_justificacion"},
                        {"response": "utter_requerir_mas"}]

        
        if intent_name == "retiro_total__motivos_procede":
                    responses = [{"response": "utter_retiro_total__motivos_procede"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "retiro_total__procedimiento":
            responses = [{"response": "utter_retiro_total__procedimiento"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "reserva_matricula__procedimiento":
            responses = [{"response": "utter_reserva_matricula__procedimiento"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "reincorporacion__procedimiento":
                    responses = [{"response": "utter_reincorporacion__procedimiento"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "constancia_matricula__solicitud_procedimiento":
            responses = [{"response": "utter_constancia_matricula__solicitud_procedimiento"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "constancia_de_notas__procedimiento":
            responses = [{"response": "utter_constancia_de_notas__procedimiento"},
                        {"response": "utter_requerir_mas"}]

        if intent_name == "constancia_de_estudios__procedimiento":
                    responses = [{"response": "utter_constancia_de_estudios__procedimiento"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "horario_atencion_aera":
            responses = [{"response": "utter_horario_atencion_aera"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "solicitud_correo_institucional_procedimiento":
            responses = [{"response": "utter_solicitud_correo_institucional_procedimiento"},
                        {"response": "utter_requerir_mas"}]


        if intent_name == "retiro_parcial__cursos_repetidos":
                    responses = [{"response": "utter_retiro_parcial__cursos_repetidos"},
                                {"response": "utter_requerir_mas"}]

    
        if intent_name == "fuera_alcance":
            responses = [{"response": "utter_fuera_alcance"},
                        {"response": "utter_requerir_mas"}]

        ## FAQ        
        #elif ("utter_" + intent_name) in utter_responses.keys():
        #    responses = [{"response": "utter_" + intent_name},
        #                 {"response": "utter_requerir_mas"}]
        
        if intent_name == "procedimiento_tramites_fechas":
            last_entities = last_message_user['entities']
            if len(last_entities) == 0:
                responses = [{"response": "utter_requerir_entidad_procedimiento_fechas"}]
            else:
                entity_value = last_entities[0]["value"]

                entity, score = matching_entity(entity_value, ENTITIES_PROCEDIMIENTOS + ENTITIES_CONSTANCIAS)
                
                if score < 0.6:
                    responses = [{"response":"utter_fuera_alcance_procedimiento_tramite"},
                                 {"response": "utter_recuerda_escribir_ayuda"},
                                 {"response": "utter_sugerir_contactar_aera"}
                                ]
                    return responses

                if entity == "retiro_total":
                    responses = [{"response": "utter_retiro_total__fechas"},
                                  {"response": "utter_requerir_mas"}]

                elif entity == "retiro_parcial":
                    responses = [{"response": "utter_retiro_parcial__fechas"},
                                  {"response": "utter_requerir_mas"}]
                
                elif entity == "reincorporacion":
                    responses = [{"response":"utter_reincorporacion__fechas"},
                                 {"response": "utter_requerir_mas"}]
                
                elif entity == "reserva_matricula":
                    responses = [{"response":"utter_reserva_matricula__fechas"},
                                  {"response": "utter_requerir_mas"}]
                
                else:
                    responses = [{"response":"utter_fuera_alcance_procedimiento_tramite"},
                                 {"response": "utter_recuerda_escribir_ayuda"},
                                 {"response": "utter_sugerir_contactar_aera"}
                                  ]
                return responses

            return last_entities

        return responses

    def next_responses(self, intent_name, intent_score, entities, session_id):
        
        last_message_user = DialogTracker.get_last_user_message(session_id)
        last_message_bot = DialogTracker.get_last_bot_message(session_id)

        responses = self.inference_rules(intent_name, intent_score, entities, last_message_user, last_message_bot)
        return responses
