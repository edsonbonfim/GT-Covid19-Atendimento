from datetime import datetime
from dao.atendimento import AtendimentoBuilder
from flask_login import current_user
from controller.formfuncs import *

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

def registrar(form, id_primeiro, id_paciente):

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    data=datetime.today()
    id_admsaude =current_user.id
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    builder = None
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    print('atendimento: ' + form['has_atendimento'])

    has_atendimento = True if form['has_atendimento'] == '1' else False

    print('has_atendimento: {}'.format(has_atendimento))

    if not has_atendimento:

        # ============ Tentativa ============

        # Comentei algumas coisas porque aparentemente so teremos uma tentativa

        raw_tentativas = form['tentativas'].split(',')

        # Retorna as chaves da tabela de domínio (list<int>)
        # ex.: [0, 1]
        real_tentativas = get_real_data(raw_tentativas)
        # real_tentativas = data_or_null(form['tentativas'])

        print('real_tentativas: {}'.format(real_tentativas))

        # Retorna as outras opções que não estão na tabela de domínio (list<str>)
        # ex.: ['Paciente saiu para buscar o filho na escola']
        others_tentativas = get_others_data(raw_tentativas)

        print('others_tentativas: {}'.format(others_tentativas))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        builder = AtendimentoBuilder(False, data, id_paciente, has_atendimento, id_atendimento_inicial=id_primeiro,
                                        tentativa=real_tentativas, others_tentativas = others_tentativas)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    else:
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        builder = AtendimentoBuilder(False, data, id_paciente, has_atendimento, id_atendimento_inicial=id_primeiro)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Isolamento domiciliar ==============

        mora_sozinho = data_or_null(form['mora_sozinho'], int)

        print('mora_sozinho: {}'.format(mora_sozinho))

        """ if mora_sozinho == 2:  # Não
            size = data_or_null(form['mora_sozinho_len'], int)

            parentescos = multiselect(form, 'parentesco', size)

            print('parentescos: {}'.format(parentescos))

            has_parentescos_doenca_cronica = multiselect(form, 'has_parentesco_doenca_cronica', size)

            print('has_parentescos_doenca_cronica: {}'.format(has_parentescos_doenca_cronica))

            parentescos_doenca_cronica = multiselect(form, 'parentesco_doenca_cronica', size)

            print('parentescos_doenca_cronica: {}'.format(parentescos_doenca_cronica))

            parentescos_data_primeiro_sintoma = multiselect(form, 'parentesco_data_primeiro_sintoma', size)

            print('parentescos_data_primeiro_sintoma: {}'.format(parentescos_data_primeiro_sintoma))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Falta inserir a doença cronica!!!
            for parentesco in parentescos:
                builder.inserirParentesco(parentesco)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # """

        # ============== Visitas ==============

        recebeu_visita = data_or_null(form['recebeu_visita'], int)

        print('recebeu_visita: {}'.format(recebeu_visita))

        if recebeu_visita == 1:  # Sim
            size = data_or_null(form['recebeu_visita_len'], int)

            visitas = multiselect(form, 'visita', size)

            print('visitas: {}'.format(visitas))

            pqs_visita = multiselect(form, 'pq_visita', size)

            print('pqs_visita: {}'.format(pqs_visita))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            for visita, motivo in zip(visitas, pqs_visita):
                builder.inserirVisita(visita, motivo)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Isolamento domiciliar ==============

        cuidado_sair_casa = data_or_null(form['cuidado_sair_casa'])

        print('cuidado_sair_casa: {}'.format(cuidado_sair_casa))

        has_isolamento = data_or_null(form['has_isolamento'], int)

        print('has_isolamento: {}'.format(has_isolamento))

        if has_isolamento == 1:  # Sim
            isolamento = data_or_null(form['isolamento'])

            print('isolamento: {}'.format(isolamento))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            builder.inserirIsolamento(True, isolamento, cuidado_sair_casa)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        elif has_isolamento == 2:  # Não
            nao_isolamento = data_or_null(form['nao_isolamento'])

            print('nao_isolamento: {}'.format(nao_isolamento))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            builder.inserirIsolamento(False, nao_isolamento, cuidado_sair_casa)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        mantem_quarentena = data_or_null(form['mantem_quarentena'], int)

        print('mantem_quarentena: {}'.format(mantem_quarentena))

        if mantem_quarentena == 1:  # Sim
            dias_quarentena = data_or_null(form['dias_quarentena'], int)

            print('dias_quarentena: {}'.format(dias_quarentena))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            builder.inserirManterEmCasa(True, dias_quarentena)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        elif mantem_quarentena == 2:  # Não
            raw_motivo_sair = form['motivo_sair'].split(',')

            real_motivo_sair = get_real_data(raw_motivo_sair)

            print('real_motivo_sair: {}'.format(real_motivo_sair))

            others_motivo_sair = get_others_data(raw_motivo_sair)

            print('others_motivo_sair: {}'.format(others_motivo_sair))

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            builder.inserirManterEmCasa(False)

            for motivo in real_motivo_sair:
                builder.inserirMotivosSair(motivo)  # , others_motivo_sair)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #



        # ============== Sintomas COVID ==============

        has_sintomas = data_or_null(form['has_sintoma'], int)

        print('has_sintomas: {}'.format(mantem_quarentena))

        #VERIFICAR COMO ESSAS INFOS ESTÃO VINDO PARA CADASTRAR
        if has_sintomas == 1:  # Sim

            size = data_or_null(form['has_sintoma_len'], int)

            real_sintomas = multiselect(form, 'apresentou_sintoma', size)
            
            real_sintoma_medicamento = multiselect(form, 'sintoma_medicamento', size)

            real_quem_indicou_medicamento = multiselect(form, 'quem_indicou_medicamento', size)

            real_dosagem = multiselect(form, 'dosagem', size)


            for i in range(size):
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
                builder.inserirSintoma(real_sintomas[i], real_sintoma_medicamento[i],
                                        real_quem_indicou_medicamento[i], real_dosagem[i])
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

        # ============== Orientações Finais ==============

        orientacao_final = format_real_data(form['orientacao_final'])

        print(orientacao_final)

        anotacao_orientacoes = data_or_null(form['anotar_orientacoes_finais'])

        print(anotacao_orientacoes)

        builder.inserirOrientacaoFinal(orientacao_final, anotacao_orientacoes)


    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    builder.finalizarPersistencia(id_admsaude, id_paciente)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #